"""
Resource utilities for the Guess The Number Game.
Contains reusable resource loading functions with fallbacks.
"""

import os
import sys
from pathlib import Path
from typing import Optional

import pygame

from config import GameConfig
from logger import get_logger

log = get_logger("utils.resources")


def get_resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource, works for dev and for PyInstaller.

    Args:
        relative_path: The relative path to the resource (e.g. 'assets/icon.png')

    Returns:
        The absolute path to the resource as a string
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS  # type: ignore
    except Exception:
        # If running in development, use the project root
        base_path = Path(__file__).parent.parent

    return os.path.join(base_path, relative_path)


def load_font_with_fallback(
    font_size: int, font_path: Optional[str] = None
) -> pygame.font.Font:
    """
    Load a custom font with fallback to system font if loading fails.

    Args:
        font_size: Size of the font to load
        font_path: Path to the font file (defaults to GameConfig.DEFAULT_FONT_PATH if None)

    Returns:
        Loaded font (either custom or system fallback)
    """
    if font_path is None:
        font_path = GameConfig.DEFAULT_FONT_PATH

    try:
        resolved_path = get_resource_path(font_path)
        font = pygame.font.Font(resolved_path, font_size)
        log.debug(f"Font loaded successfully: {font_path} (size {font_size})")
        return font
    except (
        Exception,
        FileNotFoundError,
    ) as e:  # Using generic Exception to catch pygame-related errors
        # Fallback to system font if custom font fails to load
        log.warning(
            f"Could not load font from {
                font_path} (size {font_size}), using system font fallback: {e}"
        )
        return pygame.font.SysFont(GameConfig.DEFAULT_FONT, font_size)


def load_image_with_fallback(
    image_path: str, width: Optional[int] = None, height: Optional[int] = None
) -> pygame.Surface:
    """
    Load an image with fallback to placeholder if loading fails.

    Args:
        image_path: Path to the image file
        width: Optional width to resize to
        height: Optional height to resize to

    Returns:
        Loaded pygame surface (either actual image or placeholder)
    """
    try:
        resolved_path = get_resource_path(image_path)
        loaded_image = pygame.image.load(resolved_path).convert_alpha()

        # Resize if dimensions are specified
        if width and height:
            loaded_image = pygame.transform.scale(
                loaded_image, (width, height))

        return loaded_image
    except Exception:  # Using general Exception to catch pygame-related errors
        # Create a placeholder surface if image fails to load
        placeholder = pygame.Surface((50, 50), pygame.SRCALPHA)
        # Draw a red rectangle to indicate missing image
        pygame.draw.rect(placeholder, (255, 0, 0), pygame.Rect(0, 0, 50, 50))
        log.warning(f"Could not load image from {
                    image_path}, using placeholder")
        return placeholder


def load_sound_with_fallback(
    filepath: str, name: Optional[str] = None
) -> Optional[pygame.mixer.Sound]:
    """
    Load a sound with error handling and fallback.

    Args:
        filepath: Path to the sound file
        name: Optional name for logging purposes

    Returns:
        Loaded sound object or None if loading failed
    """
    try:
        resolved_path = get_resource_path(filepath)
        sound = pygame.mixer.Sound(resolved_path)
        if name:
            log.debug(f"Sound loaded successfully: {name} from {filepath}")
        else:
            log.debug(f"Sound loaded successfully: {filepath}")
        return sound
    except Exception as e:
        sound_name = name if name else filepath
        log.error(f"Could not load sound {sound_name}: {e}")
        return None
