"""Base configuration models using Pydantic."""

from typing import Tuple

from pydantic import BaseModel, field_validator


class WindowConfig(BaseModel):
    """Configuration for window settings."""

    width: int = 640
    height: int = 400
    fps: int = 60
    title: str = "Guess The Number"

    @field_validator("width", "height")
    @classmethod
    def validate_dimension(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Window dimensions must be positive")
        return v


class GameRangeConfig(BaseModel):
    """Configuration for game number range settings."""

    min_number: int = 1
    max_number: int = 100

    @field_validator("max_number")
    @classmethod
    def validate_range(cls, v: int, values) -> int:
        if "min_number" in values.data and v <= values.data["min_number"]:
            raise ValueError("max_number must be greater than min_number")
        return v


class ColorConfig(BaseModel):
    """Configuration for color settings."""

    background_color: Tuple[int, int, int] = (30, 30, 30)  # Dark gray
    text_color: Tuple[int, int, int] = (255, 255, 255)  # White
    hint_color: Tuple[int, int, int] = (200, 200, 200)  # Light gray
    success_color: Tuple[int, int, int] = (150, 255, 150)  # Light green
    error_color: Tuple[int, int, int] = (200, 180, 180)  # Light red
    button_bg_color: Tuple[int, int, int] = (220, 220, 220)  # Light gray
    button_hover_color: Tuple[int, int, int] = (200, 200, 255)  # Light blue

    # Color defaults for components
    label_default_color: Tuple[int, int, int] = (255, 255, 255)
    h1_default_color: Tuple[int, int, int] = (255, 255, 255)
    h2_default_color: Tuple[int, int, int] = (255, 255, 255)
    h3_default_color: Tuple[int, int, int] = (255, 255, 255)
    progress_bar_bg_color: Tuple[int, int, int] = (100, 100, 100)
    progress_bar_fill_color: Tuple[int, int, int] = (0, 200, 0)
    input_underline_color: Tuple[int, int, int] = (100, 100, 100)
    # Text color when button is inactive
    inactive_button_grayed_color: Tuple[int, int, int] = (100, 100, 100)
    # Background color for inactive buttons
    inactive_button_bg_color: Tuple[int, int, int] = (150, 150, 150)

    active_button_text_color: Tuple[int, int, int] = (0, 0, 0)
    progress_bar_border_color: Tuple[int, int, int] = (255, 255, 255)

    @field_validator("*", mode="before")
    @classmethod
    def validate_color(cls, v) -> Tuple[int, int, int]:
        if isinstance(v, (list, tuple)) and len(v) == 3:
            r, g, b = v
            if all(isinstance(c, int) and 0 <= c <= 255 for c in (r, g, b)):
                return (r, g, b)
        raise ValueError("Color must be a tuple of 3 integers between 0 and 255")
