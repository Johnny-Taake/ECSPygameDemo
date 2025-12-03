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

    # Logging settings
    log_level: Optional[LogLevel] = None

    # Difficulty settings
    difficulty_default_index: Optional[int] = None

    # Stats settings
    stats_encryption_key: Optional[str] = None
    stats_file_name: Optional[str] = None
    stats_app_data_dir_name: Optional[str] = None
    stats_max_top_attempts: Optional[int] = None

    # UI settings
    scene_max_win_top_scores: Optional[int] = None

    def get_config(self) -> GameConfig:
        """Get the game configuration, potentially modified by environment variables."""
        config = GameConfig()

        # Override with environment variables if provided
        if self.window_fps is not None:
            config.window.fps = self.window_fps
        if self.window_title is not None:
            config.window.title = self.window_title
        if self.log_level is not None:
            config.logging.log_level = self.log_level
        if self.difficulty_default_index is not None:
            config.difficulty.default_index = self.difficulty_default_index
        if self.stats_encryption_key is not None:
            config.stats.encryption_key = self.stats_encryption_key
        if self.stats_file_name is not None:
            config.stats.stats_file_name = self.stats_file_name
        if self.stats_app_data_dir_name is not None:
            config.stats.app_data_dir_name = self.stats_app_data_dir_name
        if self.stats_max_top_attempts is not None:
            config.stats.max_top_attempts = self.stats_max_top_attempts
        if self.scene_max_win_top_scores is not None:
            config.ui.scene_max_win_top_scores = self.scene_max_win_top_scores

        return config


# Global instance for easy access
settings = Settings()
