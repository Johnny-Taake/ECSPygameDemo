"""
Utility functions for the Guess The Number Game.
"""

__all__ = [
    "apply_alpha",
    "scale_text_to_width",
    "format_timestamp",
    "is_signed_integer",
    "is_positive_integer",
    "is_in_range",
    "is_point_in_rect",
    "load_font_with_fallback",
    "load_image_with_fallback",
    "load_sound_with_fallback",
    "ResponsiveScaleManager",
    "get_resource_path",
    "resource_exists",
]


from .graphics import apply_alpha, scale_text_to_width
from .helpers import (
    format_timestamp,
    is_signed_integer,
    is_positive_integer,
    is_in_range,
    is_point_in_rect,
)
from .responsive import ResponsiveScaleManager
from .resources import get_resource_path, resource_exists
from .resources_extended import (
    load_font_with_fallback,
    load_image_with_fallback,
    load_sound_with_fallback,
)
