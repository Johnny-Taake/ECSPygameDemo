"""Custom colored formatter for logging that colors only the log level tags."""

import logging
from typing import Literal
import colorama


class ColoredFormatter(logging.Formatter):
    """A logging formatter that adds colors to log level tags while keeping the rest of the message uncolored."""

    def __init__(
        self, fmt=None, datefmt=None, style: Literal["%", "{", "$"] = "%", validate=True
    ):
        colorama.init(autoreset=True, strip=False)

        # ANSI color codes using colorama constants
        self.COLORS = {
            "DEBUG": colorama.Fore.CYAN,
            "INFO": colorama.Fore.GREEN,
            "WARNING": colorama.Fore.YELLOW,
            "ERROR": colorama.Fore.RED,
            "CRITICAL": colorama.Fore.MAGENTA,
            "RESET": colorama.Style.RESET_ALL,
        }

        super().__init__(fmt, datefmt, style, validate)

    def format(self, record):
        """Format the log record with colored level name."""
        original_format = super().format(record)

        levelname = record.levelname
        if levelname in self.COLORS:
            colored_levelname = (
                f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
            )
            return original_format.replace(
                f" - {levelname} - ", f" - {colored_levelname} - ", 1
            )

        return original_format
