__all__ = ["setup_logging", "get_logger", "ColoredFormatter"]

import logging

from pathlib import Path
from config import GameConfig
from .colored_formatter import ColoredFormatter


def setup_logging():
    """Configure logging based on the game configuration."""
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Clear any existing handlers to prevent duplicates on multiple calls
    root_logger = logging.getLogger()
    if root_logger.handlers:
        root_logger.handlers.clear()

    # Create file handler that overwrites the log file each time (without colors)
    file_handler = logging.FileHandler(f"{GameConfig.logging.logs_dir}/app.log", mode="w")
    file_formatter = logging.Formatter(GameConfig.LOG_FORMAT)
    file_handler.setFormatter(file_formatter)

    # Create console handler for stdout with colored formatter
    console_handler = logging.StreamHandler()
    console_formatter = ColoredFormatter(GameConfig.LOG_FORMAT)
    console_handler.setFormatter(console_formatter)

    # Configure the root logger
    root_logger.setLevel(GameConfig.LOG_LEVEL)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


def get_logger(name: str):
    """Get a logger with the specified name."""
    return logging.getLogger(name)
