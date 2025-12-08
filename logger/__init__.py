__all__ = ["setup_logging", "get_logger", "ColoredFormatter"]

import logging
from pathlib import Path

from config import GameConfig
from .colored_formatter import ColoredFormatter


def setup_logging():
    """Configure logging based on the game configuration."""

    root_logger = logging.getLogger()
    root_logger.handlers.clear()

    # Console handler (always enabled)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColoredFormatter(GameConfig.LOG_FORMAT))
    root_logger.addHandler(console_handler)

    # Optional file handler
    if GameConfig.logging.write_to_file:
        log_dir = Path(GameConfig.logging.logs_dir)
        log_dir.mkdir(exist_ok=True)

        file_handler = logging.FileHandler(log_dir / "app.log", mode="w")
        file_handler.setFormatter(logging.Formatter(GameConfig.LOG_FORMAT))
        root_logger.addHandler(file_handler)

    root_logger.setLevel(GameConfig.LOG_LEVEL)


def get_logger(name: str):
    """Get a logger with the specified name."""
    return logging.getLogger(name)
