"""Statistics manager for the Guess the Number game."""

import datetime
import atexit
from dataclasses import asdict
from typing import Any, Dict

from config import GameConfig
from logger import get_logger
from stats.models import GameResult
from stats.storage import (
    load_stats_from_file,
    save_stats_to_file,
    get_stats_file_path,
    IS_FROZEN,
)


log = get_logger("stats.manager")


class StatsManager:
    """Manages game statistics with executable-compatible persistence."""

    def __init__(self):
        self._stats_file = get_stats_file_path(IS_FROZEN)
        log.debug("Stats file path resolved to: %s", self._stats_file)
        self._stats = self._load_stats()
        # Register cleanup function to save stats on exit
        atexit.register(self.save_stats)

    def _load_stats(self) -> Dict[str, Any]:
        """Load statistics from file."""
        loaded_stats = load_stats_from_file(self._stats_file)

        # Merge with default stats for any missing difficulties
        default_stats = self._get_default_stats()
        for key, value in default_stats.items():
            if key not in loaded_stats:
                loaded_stats[key] = value

        return loaded_stats

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

        # Add to top attempts and keep only the configured number of top attempts
        self._stats[difficulty_key]["top_attempts"].append(asdict(result))
        # Sort by attempts (ascending), and for equal attempts, by timestamp (oldest first) to ensure
        # that older games with the same attempt count keep their better ranking
        self._stats[difficulty_key]["top_attempts"].sort(
            key=lambda x: (
                x["attempts"],
                datetime.datetime.fromisoformat(x["timestamp"]).timestamp(),
            )
        )
        self._stats[difficulty_key]["top_attempts"] = self._stats[difficulty_key][
            "top_attempts"
        ][: GameConfig.STATS_MAX_TOP_ATTEMPTS]
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

    def save_stats(self) -> bool:
        """Save statistics to file."""
        return save_stats_to_file(self._stats, self._stats_file)

    def reset_stats(self):
        """Reset all statistics to default."""
        log.info("Resetting statistics to default values.")
        self._stats = self._get_default_stats()
        self.save_stats()

    def get_ranking_for_new_score(
        self, new_attempts: int, difficulty_name: str, min_num: int, max_num: int
    ) -> int:
        """Get the ranking for a new score without recording it yet."""
        difficulty_key = f"{difficulty_name}_{min_num}-{max_num}"

        if difficulty_key not in self._stats:
            # If no stats exist for this difficulty, this would be rank #1
            return 1

        top_attempts = self._stats[difficulty_key]["top_attempts"]

        # If there are no previous attempts, this is automatically rank #1
        if not top_attempts:
            return 1

        # Check the position where the new attempt would fit
        for i, attempt in enumerate(top_attempts):
            if new_attempts < attempt["attempts"]:
                # New attempt is better than this stored attempt
                return i + 1
        else:
            # If the loop completed without break, check if there's space in the list
            if len(top_attempts) < GameConfig.STATS_MAX_TOP_ATTEMPTS:
                # There's still space in the top scores
                return len(top_attempts) + 1

        # If the new score doesn't beat any in the top list, return 0
        return 0
