__all__ = ["setup_logging", "get_logger"]

import logging

from config import GameConfig


def setup_logging():
    """Configure logging based on the game configuration."""
    logging.basicConfig(
        level=GameConfig.LOG_LEVEL,
        format=GameConfig.LOG_FORMAT,
    )


def get_logger(name: str):
    """Get a logger with the specified name."""
    return logging.getLogger(name)
