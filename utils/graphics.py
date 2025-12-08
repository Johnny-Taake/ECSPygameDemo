"""
Graphics utility functions for the Guess The Number Game.
Contains reusable graphics transformation functions.
"""

from typing import Tuple
import pygame


def apply_alpha(color: Tuple[int, ...], alpha: float) -> Tuple[int, ...]:
    """
    Apply alpha transparency to a color tuple.

    Args:
        color: A tuple of color values (R, G, B) or (R, G, B, A)
        alpha: Alpha value between 0.0 and 1.0

    Returns:
        A new color tuple with alpha applied to each component
    """
    return tuple(int(c * alpha) for c in color)


def scale_text_to_width(surface, max_width: int):
    """
    Scale a text surface to fit within a maximum width while preserving aspect ratio.

    Args:
        surface: Pygame surface containing the rendered text
        max_width: Maximum width allowed for the text

    Returns:
        Either the original surface (if it fits) or a scaled surface
    """
    if surface.get_width() <= max_width:
        return surface

    # Scale the text surface down to fit within max_width
    aspect_ratio = surface.get_height() / surface.get_width()
    new_width = max_width
    new_height = int(new_width * aspect_ratio)

    return pygame.transform.smoothscale(surface, (new_width, new_height))
