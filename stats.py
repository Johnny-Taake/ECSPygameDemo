"""Game statistics module that works with executable packaging."""

from typing import Any, Dict
import json
import os
import sys
from dataclasses import dataclass, asdict
import atexit
import logging
import base64
import platform

from config import GameConfig
from logger import get_logger


log = get_logger("stats")

# Detect if we are running as a frozen executable
IS_FROZEN = getattr(sys, "frozen", False)

# Simple XOR-based "encryption" key for exe mode
_ENCRYPTION_KEY = b"GuessTheNumberPygameKey"


@dataclass
class GameResult:
    """Represents a single game result."""

    attempts: int
    difficulty: str
    min_number: int
    max_number: int
    timestamp: str  # ISO format timestamp

    def __post_init__(self):
        # Ensure attempts is an integer
        self.attempts = int(self.attempts)


def _xor_bytes(data: bytes, key: bytes) -> bytes:
    """Simple XOR over data with repeating key."""
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def _encrypt_text(plain_text: str) -> str:
    """Encrypt text for exe mode (XOR + base64)."""
    data = plain_text.encode("utf-8")
    xored = _xor_bytes(data, _ENCRYPTION_KEY)
    return base64.b64encode(xored).decode("ascii")


def _decrypt_text(cipher_text: str) -> str:
    """Decrypt text for exe mode (base64 + XOR)."""
    raw = base64.b64decode(cipher_text.encode("ascii"))
    data = _xor_bytes(raw, _ENCRYPTION_KEY)
    return data.decode("utf-8")


def _get_app_data_dir() -> str:
    """Return a platform-appropriate app data directory for the game."""
    system = platform.system()

    # Windows: %APPDATA%\GuessTheNumberPygame
    if system == "Windows":
        base_dir = os.getenv("APPDATA") or os.path.expanduser("~")
        return os.path.join(base_dir, "GuessTheNumberPygame")

    # macOS: ~/Library/Application Support/GuessTheNumberPygame
    if system == "Darwin":
        base_dir = os.path.expanduser("~/Library/Application Support")
        return os.path.join(base_dir, "GuessTheNumberPygame")

    # Linux / other: ~/.local/share/GuessTheNumberPygame
    base_dir = os.path.expanduser("~/.local/share")
    return os.path.join(base_dir, "GuessTheNumberPygame")


class StatsManager:
    """Manages game statistics with executable-compatible persistence."""

    def __init__(self):
        self._stats_file = self._get_stats_file_path()
        log.debug("Stats file path resolved to: %s", self._stats_file)
        self._stats = self._load_stats()
        # Register cleanup function to save stats on exit
        atexit.register(self.save_stats)

    def _get_stats_file_path(self) -> str:
        """Get the path for the stats file."""
        if IS_FROZEN:
            # Running as compiled executable: use application data directory
            application_path = _get_app_data_dir()
        else:
            # Running as script - get the directory containing this file (project root)
            application_path = os.path.dirname(os.path.abspath(__file__))

        return os.path.join(application_path, "game_stats.json")

    def _load_stats(self) -> Dict[str, Any]:
        """Load statistics from file."""
        if os.path.exists(self._stats_file):
            try:
                log.debug("Loading stats from file: %s", self._stats_file)
                with open(self._stats_file, "r", encoding="utf-8") as f:
                    if IS_FROZEN:
                        # Encrypted format in exe mode
                        encrypted_content = f.read()
                        if encrypted_content.strip():
                            decrypted = _decrypt_text(encrypted_content)
                            data = json.loads(decrypted)
                        else:
                            data = self._get_default_stats()
                    else:
                        # Plain JSON in script mode
                        data = json.load(f)

                    log.info("Statistics loaded successfully.")
                    return data
            except (json.JSONDecodeError, IOError, ValueError) as e:
                log.error(
                    "Error loading stats from %s: %s. "
                    "Falling back to default stats.",
                    self._stats_file,
                    e,
                )

        # Return default stats structure
        log.info("Stats file not found or invalid. Using default statistics.")
        return self._get_default_stats()

    def _get_default_stats(self) -> Dict[str, Any]:
        """Get default statistics structure."""
        stats: Dict[str, Any] = {}
        for difficulty in GameConfig.DIFFICULTY_MODES:
            difficulty_key = f"{difficulty.name}_{difficulty.min}-{difficulty.max}"
            stats[difficulty_key] = {
                "games_played": 0,
                "top_attempts": [],  # Will store GameResult objects as dicts
            }
        return stats

    def record_game(
        self, attempts: int, difficulty_name: str, min_num: int, max_num: int
    ):
        """Record a completed game."""
        import datetime

        # Create difficulty key
        difficulty_key = f"{difficulty_name}_{min_num}-{max_num}"

        # Ensure the difficulty exists in stats
        if difficulty_key not in self._stats:
            log.debug("Creating new difficulty entry for key: %s", difficulty_key)
            self._stats[difficulty_key] = {"games_played": 0, "top_attempts": []}

        # Increment games played
        self._stats[difficulty_key]["games_played"] += 1
        log.debug(
            "Incremented games_played for %s to %s",
            difficulty_key,
            self._stats[difficulty_key]["games_played"],
        )

        # Create game result
        result = GameResult(
            attempts=attempts,
            difficulty=difficulty_name,
            min_number=min_num,
            max_number=max_num,
            timestamp=datetime.datetime.now().isoformat(),
        )

        # Add to top attempts and keep only top 10
        self._stats[difficulty_key]["top_attempts"].append(asdict(result))
        # Sort by attempts (ascending) and keep top 10
        self._stats[difficulty_key]["top_attempts"].sort(key=lambda x: x["attempts"])
        self._stats[difficulty_key]["top_attempts"] = self._stats[difficulty_key][
            "top_attempts"
        ][:10]
        log.info(
            "Recorded game result for %s: attempts=%s",
            difficulty_key,
            attempts,
        )

        # Save immediately to persist data
        self.save_stats()

    def get_stats_for_difficulty(
        self, difficulty_name: str, min_num: int, max_num: int
    ) -> Dict[str, Any]:
        """Get statistics for a specific difficulty."""
        difficulty_key = f"{difficulty_name}_{min_num}-{max_num}"

        if difficulty_key in self._stats:
            return self._stats[difficulty_key]

        # Return default if not found
        return {"games_played": 0, "top_attempts": []}

    def get_all_stats(self) -> Dict[str, Any]:
        """Get all statistics."""
        return self._stats

    def save_stats(self):
        """Save statistics to file."""
        try:
            # Ensure directory exists
            directory = os.path.dirname(self._stats_file)
            if directory:
                os.makedirs(directory, exist_ok=True)

            log.debug("Saving stats to file: %s", self._stats_file)

            if IS_FROZEN:
                # Encrypted save in exe mode
                json_text = json.dumps(self._stats, indent=2, ensure_ascii=False)
                encrypted = _encrypt_text(json_text)
                with open(self._stats_file, "w", encoding="utf-8") as f:
                    f.write(encrypted)
            else:
                # Plain JSON in script mode (original behavior)
                with open(self._stats_file, "w", encoding="utf-8") as f:
                    json.dump(self._stats, f, indent=2, ensure_ascii=False)

            log.info("Statistics saved successfully.")
        except IOError as e:
            # Keep print for visibility in simple console runs + log for structured apps
            print(f"Error saving stats: {e}")
            log.error("Error saving stats to %s: %s", self._stats_file, e)

    def reset_stats(self):
        """Reset all statistics to default."""
        log.info("Resetting statistics to default values.")
        self._stats = self._get_default_stats()
        self.save_stats()


# Global instance
_stats_manager: "StatsManager | None" = None


def get_stats_manager() -> StatsManager:
    """Get the global stats manager instance."""
    global _stats_manager
    if _stats_manager is None:
        log.debug("Creating global StatsManager instance.")
        _stats_manager = StatsManager()
    return _stats_manager


def record_game_completion(
    attempts: int, difficulty_name: str, min_num: int, max_num: int
):
    """Convenience function to record a completed game."""
    manager = get_stats_manager()
    manager.record_game(attempts, difficulty_name, min_num, max_num)


def get_difficulty_stats(
    difficulty_name: str, min_num: int, max_num: int
) -> Dict[str, Any]:
    """Convenience function to get stats for a difficulty."""
    manager = get_stats_manager()
    return manager.get_stats_for_difficulty(difficulty_name, min_num, max_num)


def get_all_stats() -> Dict[str, Any]:
    """Convenience function to get all stats."""
    manager = get_stats_manager()
    return manager.get_all_stats()
