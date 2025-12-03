"""Statistics models for the Guess the Number game."""

from dataclasses import dataclass
from typing import List
import datetime


@dataclass
class GameResult:
    """Represents a single game result."""

    attempts: int
    difficulty: str
    min_number: int
    max_number: int
    timestamp: str  # ISO format timestamp

    def __post_init__(self):
        # Ensure attempts is an integer
        self.attempts = int(self.attempts)


@dataclass
class DifficultyStats:
    """Statistics for a specific difficulty level."""

    games_played: int
    top_attempts: List[GameResult]
