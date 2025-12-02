from enum import Enum, auto
from random import randint

from config import GameConfig
from logger import get_logger

log = get_logger("game/logic")


class GuessStatus(Enum):
    INVALID_FORMAT = auto()
    OUT_OF_RANGE = auto()
    TOO_LOW = auto()
    TOO_HIGH = auto()
    CORRECT = auto()


class GameLogic:
    def __init__(
        self, min_number=None, max_number=None
    ):
        # If no range is provided, use the default difficulty from config
        if min_number is None or max_number is None:
            from config import GameConfig
            default_difficulty_modes = GameConfig.DIFFICULTY_MODES
            default_index = GameConfig.DEFAULT_DIFFICULTY_INDEX
            if default_difficulty_modes and 0 <= default_index < len(default_difficulty_modes):
                default_mode = default_difficulty_modes[default_index]
                min_number = default_mode.min
                max_number = default_mode.max
            else:
                # Fallback if configuration is invalid
                log.warning("Invalid default difficulty configuration - using fallback range (1-100)")
                min_number = 1
                max_number = 100

        self.min_number = min_number
        self.max_number = max_number
        self.attempts = 0

    def generate_new_number(self):
        """Generate a new random number to guess"""
        self.number_to_guess = randint(self.min_number, self.max_number)
        log.debug("New number generated: number_to_guess=%s", self.number_to_guess)

    def reset(self):
        self.generate_new_number()
        self.attempts = 0

    def check(self, guess_str: str) -> GuessStatus:
        # First check if the input is a valid number format
        if not guess_str or not all(
            ch.isdigit() or ch == "-" for ch in guess_str.lstrip("-")
        ):
            if not guess_str:
                log.warning("INVALID_FORMAT - empty input")
            else:
                log.debug('INVALID_FORMAT input: "%s"', guess_str)
            return GuessStatus.INVALID_FORMAT

        try:
            guess = int(guess_str)
        except ValueError:
            log.debug('INVALID_FORMAT input (not a valid integer): "%s"', guess_str)
            return GuessStatus.INVALID_FORMAT

        # Check if the number is within the valid range
        if guess < self.min_number or guess > self.max_number:
            log.debug(
                "OUT_OF_RANGE input: %s (valid range: %s-%s)",
                guess,
                self.min_number,
                self.max_number,
            )
            return GuessStatus.OUT_OF_RANGE

        # Only count valid attempts within the range
        self.attempts += 1
        log.info("Attempt #%s, guess = %s", self.attempts, guess)

        match guess:
            case g if g < self.number_to_guess:
                return GuessStatus.TOO_LOW
            case g if g > self.number_to_guess:
                return GuessStatus.TOO_HIGH
            case _:
                return GuessStatus.CORRECT
