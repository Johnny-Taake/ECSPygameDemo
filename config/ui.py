"""UI configuration models using Pydantic."""

from typing import Tuple

from pydantic import BaseModel, field_validator


class UIConfig(BaseModel):
    """Configuration for UI settings."""

    default_font: str = "arial"
    default_font_size: int = 18
    button_padding: int = 12
    button_radius: int = 10

    # Font sizes for headers
    h1_font_size: int = 36
    h2_font_size: int = 28
    h3_font_size: int = 24

    # Progress bar settings
    progress_bar_border_radius: int = 3

    # Input field settings
    input_field_default_max_length: int = 6

    # Component animation speeds
    progress_bar_animation_speed: float = 8.0
    alpha_animation_speed: float = 6.0

    # Scene settings
    scene_max_history_entries: int = 6
    scene_title_position: Tuple[int, int] = (300, 80)
    scene_subtitle_position: Tuple[int, int] = (300, 130)
    scene_button_start_position: Tuple[int, int] = (300, 240)
    scene_button_exit_position: Tuple[int, int] = (300, 300)

    # Input field settings
    input_field_width: int = 300
    input_field_font_size: int = 28
    input_mouse_detection_width: int = 120
    input_mouse_detection_height: int = 20

    @field_validator(
        "default_font_size",
        "h1_font_size",
        "h2_font_size",
        "h3_font_size",
        "button_padding",
        "button_radius",
        "progress_bar_border_radius",
        "input_field_default_max_length",
        "scene_max_history_entries",
    )
    @classmethod
    def validate_positive_int(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Value must be positive")
        return v

    @field_validator("progress_bar_animation_speed", "alpha_animation_speed")
    @classmethod
    def validate_positive_float(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Value must be positive")
        return v
