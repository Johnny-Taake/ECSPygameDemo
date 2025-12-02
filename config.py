"""Configuration module for the Guess The Number game."""

import logging


class GameConfig:
    """Configuration class containing all game settings."""

    # Window settings
    WINDOW_WIDTH = 640
    WINDOW_HEIGHT = 400
    FPS = 60
    WINDOW_TITLE = "Guess The Number"

    # Game settings
    MIN_NUMBER = 1
    MAX_NUMBER = 100

    # Colors
    BACKGROUND_COLOR = (30, 30, 30)  # Dark gray
    TEXT_COLOR = (255, 255, 255)  # White
    HINT_COLOR = (200, 200, 200)  # Light gray
    SUCCESS_COLOR = (150, 255, 150)  # Light green
    ERROR_COLOR = (200, 180, 180)  # Light red
    BUTTON_BG_COLOR = (220, 220, 220)  # Light gray
    BUTTON_HOVER_COLOR = (200, 200, 255)  # Light blue

    # UI settings
    DEFAULT_FONT = "arial"
    DEFAULT_FONT_SIZE = 18
    BUTTON_PADDING = 12
    BUTTON_RADIUS = 10

    # Logging
    LOG_LEVEL = logging.DEBUG
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Scene settings
    SCENE_TITLE_POSITION = (300, 80)
    SCENE_SUBTITLE_POSITION = (300, 130)
    SCENE_BUTTON_START_POSITION = (300, 240)
    SCENE_BUTTON_EXIT_POSITION = (300, 300)
    SCENE_MAX_HISTORY_ENTRIES = 6
