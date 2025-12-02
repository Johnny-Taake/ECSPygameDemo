from enum import Enum, auto
from random import randint

import logging

log = logging.getLogger("game/logic")


class GuessStatus(Enum):
    INVALID = auto()
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
        if not guess_str or not any(ch.isdigit() for ch in guess_str):
            if not guess_str:
                log.warning("INVALID - empty input")

            else:
                log.debug("INVALID input: \"%s\"", guess_str)
            return GuessStatus.INVALID

        guess = int(guess_str)
        self.attempts += 1

        log.info("Attempt #%s, guess = %s", self.attempts, guess)

        match guess:
            case g if g < self.number_to_guess:
                return GuessStatus.TOO_LOW
            case g if g > self.number_to_guess:
                return GuessStatus.TOO_HIGH
            case _:
                return GuessStatus.CORRECT
