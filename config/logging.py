"""Logging configuration models using Pydantic."""

from typing import Literal
from pathlib import Path

import logging
from pydantic import BaseModel, field_validator

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class LoggingConfig(BaseModel):
    """Configuration for logging settings."""

    log_level: LogLevel = "DEBUG"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logs_dir: str = "logs"

    @property
    def log_level_enum(self) -> int:
        """Convert the log level string to the corresponding logging enum."""
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        return level_map[self.log_level]

    @field_validator("logs_dir")
    @classmethod
    def validate_positive_float(cls, v: str) -> str:
        Path(v).mkdir(exist_ok=True)
        return v
