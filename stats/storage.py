"""Statistics storage module with encryption support for executable packaging."""

import base64
import json
import os
import platform
import sys
from typing import Any, Dict
from pathlib import Path

from config import GameConfig
from logger import get_logger


log = get_logger("stats.storage")

# Detect if we are running as a frozen executable
IS_FROZEN = getattr(sys, "frozen", False)

# Simple XOR-based "encryption" key for exe mode
_ENCRYPTION_KEY = GameConfig.STATS_ENCRYPTION_KEY.encode("utf-8")


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

    # Windows: %APPDATA%\[AppName]
    if system == "Windows":
        base_dir = os.getenv("APPDATA") or os.path.expanduser("~")
        return os.path.join(base_dir, GameConfig.STATS_APP_DATA_DIR_NAME)

    # macOS: ~/Library/Application Support/[AppName]
    if system == "Darwin":
        base_dir = os.path.expanduser("~/Library/Application Support")
        return os.path.join(base_dir, GameConfig.STATS_APP_DATA_DIR_NAME)

    # Linux / other: ~/.local/share/[AppName]
    base_dir = os.path.expanduser("~/.local/share")
    return os.path.join(base_dir, GameConfig.STATS_APP_DATA_DIR_NAME)


def load_stats_from_file(file_path: str) -> Dict[str, Any]:
    """Load statistics from the specified file."""
    if os.path.exists(file_path):
        try:
            log.debug("Loading stats from file: %s", file_path)
            with open(file_path, "r", encoding="utf-8") as f:
                if IS_FROZEN:
                    # Encrypted format in exe mode
                    encrypted_content = f.read()
                    if encrypted_content.strip():
                        decrypted = _decrypt_text(encrypted_content)
                        data = json.loads(decrypted)
                    else:
                        data = {}
                else:
                    # Plain JSON in script mode
                    data = json.load(f)

                log.info("Statistics loaded successfully.")
                return data
        except (json.JSONDecodeError, IOError, ValueError) as e:
            log.error(
                "Error loading stats from %s: %s. " "Falling back to empty stats.",
                file_path,
                e,
            )

    # Return empty stats structure if file doesn't exist or is invalid
    log.info("Stats file not found or invalid. Returning empty statistics.")
    return {}


def save_stats_to_file(stats: Dict[str, Any], file_path: str) -> bool:
    """Save statistics to the specified file."""
    try:
        # Ensure directory exists
        directory = os.path.dirname(file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        log.debug("Saving stats to file: %s", file_path)

        if IS_FROZEN:
            # Encrypted save in exe mode
            json_text = json.dumps(stats, indent=2, ensure_ascii=False)
            encrypted = _encrypt_text(json_text)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(encrypted)
        else:
            # Plain JSON in script mode
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)

        log.info("Statistics saved successfully.")
        return True
    except IOError as e:
        # Keep print for visibility in simple console runs + log for structured apps
        print(f"Error saving stats: {e}")
        log.error("Error saving stats to %s: %s", file_path, e)
        return False


def get_stats_file_path(is_frozen: bool) -> str:
    """Get the path for the stats file."""
    if is_frozen:
        # Running as compiled executable: use application data directory
        application_path = _get_app_data_dir()
    else:
        # Running as script - get the directory containing this file (project root)
        application_path = Path(__file__).resolve().parent.parent

    return os.path.join(application_path, GameConfig.STATS_FILE_NAME)
