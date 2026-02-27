"""Configuration module for the Guess The Number game using Pydantic."""

__all__ = ["GameConfig", "settings"]


from .settings import settings

_game_config_instance = settings.get_config()


def get_config():
    """Get the global configuration instance."""
    return _game_config_instance


GameConfig = _game_config_instance
