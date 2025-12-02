from enum import Enum, auto
from random import randint

import logging

log = logging.getLogger("game/logic")


class GuessStatus(Enum):
    INVALID_FORMAT = auto()
    OUT_OF_RANGE = auto()
    TOO_LOW = auto()
    TOO_HIGH = auto()
    CORRECT = auto()


class GameLogic:
    def __init__(self, min_number=1, max_number=100):
        self.min_number = min_number
        self.max_number = max_number
        self.number_to_guess = randint(self.min_number, self.max_number)
        self.attempts = 0

        log.debug("GameLogic initialized: number_to_guess=%s",
                  self.number_to_guess)

    def reset(self):
        self.number_to_guess = randint(self.min_number, self.max_number)
        self.attempts = 0

        log.debug("GameLogic reset: number_to_guess=%s", self.number_to_guess)

    def check(self, guess_str: str) -> GuessStatus:
        # First check if the input is a valid number format
        if not guess_str or not all(ch.isdigit() or ch == '-' for ch in guess_str.lstrip('-')):
            if not guess_str:
                log.warning("INVALID_FORMAT - empty input")
            else:
                log.debug("INVALID_FORMAT input: \"%s\"", guess_str)
            return GuessStatus.INVALID_FORMAT

        try:
            guess = int(guess_str)
        except ValueError:
            log.debug("INVALID_FORMAT input (not a valid integer): \"%s\"", guess_str)
            return GuessStatus.INVALID_FORMAT

        # Check if the number is within the valid range
        if guess < self.min_number or guess > self.max_number:
            log.debug("OUT_OF_RANGE input: %s (valid range: %s-%s)", guess, self.min_number, self.max_number)
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
