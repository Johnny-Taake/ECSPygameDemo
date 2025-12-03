"""Statistics configuration models using Pydantic."""

from typing import Optional
from pydantic import BaseModel, field_validator


class StatsConfig(BaseModel):
    """Configuration for statistics and high score system."""

    # Encryption settings
    encryption_key: str = "GuessTheNumberPygameKey"

    # Stats file settings
    stats_file_name: str = "game_stats.json"
    app_data_dir_name: str = "GuessTheNumberPygame"

    # High scores settings
    max_top_attempts: int = 10  # Maximum number of top scores to keep per difficulty

    @field_validator("max_top_attempts")
    @classmethod
    def validate_max_top_attempts(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Maximum top attempts must be positive")
        return v

    @field_validator("stats_file_name", "app_data_dir_name")
    @classmethod
    def validate_path_component(cls, v: str) -> str:
        if v and any(c in v for c in ["<", ">", ":", '"', "|", "?", "*", "\\", "/"]):
            raise ValueError("Path component contains invalid characters")
        return v
