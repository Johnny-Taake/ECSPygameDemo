"""Settings configuration using pydantic-settings."""

from typing import Optional, Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

from .game_config import GameConfig

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(env_file=".env", env_prefix="GAME_")

    window_fps: Optional[int] = None
    window_title: Optional[str] = None

    game_min_number: Optional[int] = None
    game_max_number: Optional[int] = None

    # Logging settings
    log_level: Optional[LogLevel] = None

    def get_config(self) -> GameConfig:
        """Get the game configuration, potentially modified by environment variables."""
        config = GameConfig()

        # Override with environment variables if provided
        if self.window_fps is not None:
            config.window.fps = self.window_fps
        if self.window_title is not None:
            config.window.title = self.window_title
        if self.game_min_number is not None:
            config.game_range.min_number = self.game_min_number
        if self.game_max_number is not None:
            config.game_range.max_number = self.game_max_number
        if self.log_level is not None:
            config.logging.log_level = self.log_level

        return config


# Global instance for easy access
settings = Settings()
