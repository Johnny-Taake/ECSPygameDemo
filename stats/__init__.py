"""Game statistics module that works with executable packaging."""

from stats.manager import StatsManager
from stats.models import GameResult


# Global instance
_stats_manager = None


def get_stats_manager():
    """Get the global stats manager instance."""
    global _stats_manager
    if _stats_manager is None:
        from stats.manager import StatsManager

        _stats_manager = StatsManager()
    return _stats_manager


def record_game_completion(
    attempts: int, difficulty_name: str, min_num: int, max_num: int
):
    """Convenience function to record a completed game."""
    manager = get_stats_manager()
    manager.record_game(attempts, difficulty_name, min_num, max_num)


def get_difficulty_stats(difficulty_name: str, min_num: int, max_num: int) -> dict:
    """Convenience function to get stats for a difficulty."""
    manager = get_stats_manager()
    return manager.get_stats_for_difficulty(difficulty_name, min_num, max_num)


def get_all_stats() -> dict:
    """Convenience function to get all stats."""
    manager = get_stats_manager()
    return manager.get_all_stats()


# For backward compatibility
__all__ = [
    "StatsManager",
    "GameResult",
    "get_stats_manager",
    "record_game_completion",
    "get_difficulty_stats",
    "get_all_stats",
]
