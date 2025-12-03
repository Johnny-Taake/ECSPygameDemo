"""Base configuration models using Pydantic."""

from typing import List, Tuple
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


class ColorConfig(BaseModel):
    """Configuration for color settings."""

    background_color: Tuple[int, int, int] = (30, 30, 30)  # Dark gray
    text_color: Tuple[int, int, int] = (255, 255, 255)  # White
    hint_color: Tuple[int, int, int] = (200, 200, 200)  # Light gray
    shortcut_tag_color: Tuple[int, int, int] = (100, 100, 100)  # Medium gray for shortcut tags
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


class DifficultyModel(BaseModel):
    """Model for a single difficulty setting."""
    name: str
    min: int
    max: int

    @field_validator("max")
    @classmethod
    def validate_difficulty_range(cls, v: int, values) -> int:
        if "min" in values.data and v <= values.data["min"]:
            raise ValueError("max must be greater than min")
        return v


class DifficultyConfig(BaseModel):
    """Configuration for all difficulty modes."""
    modes: List[DifficultyModel] = [
        DifficultyModel(name="Easy", min=1, max=10),
        DifficultyModel(name="Medium", min=1, max=100),
        DifficultyModel(name="Hard", min=1, max=1000),
        DifficultyModel(name="Very Hard", min=1, max=10000),
        DifficultyModel(name="Extreme", min=1, max=100000)
    ]
    default_index: int = 1  # Index of default difficulty mode (0-based), defaulting to "Medium" at index 1

    @field_validator("modes")
    @classmethod
    def validate_modes(cls, v: List[DifficultyModel]) -> List[DifficultyModel]:
        if not v:
            raise ValueError("At least one difficulty mode must be defined")
        return v

    @field_validator("default_index")
    @classmethod
    def validate_default_index(cls, v: int, values) -> int:
        if "modes" in values.data and v >= len(values.data["modes"]):
            raise ValueError(f"Default index {v} is out of range for {len(values.data['modes'])} difficulty modes")
        if v < 0:
            raise ValueError("Default index must be non-negative")
        return v
