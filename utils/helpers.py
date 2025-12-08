"""
General helper functions for the Guess The Number Game.
Contains reusable utility functions.
"""

from datetime import datetime
import sys
from typing import Union


def format_timestamp(ts: str) -> str:
    """
    Convert ISO timestamp into short readable format: 3 Dec'25

    Args:
        ts: ISO format timestamp string

    Returns:
        Formatted timestamp string like '3 Dec'25'
    """
    dt = datetime.fromisoformat(ts)
    return (
        dt.strftime("%-d %b '%y")
        if sys.platform != "win32"
        else dt.strftime("%#d %b'%y")
    )


def is_signed_integer(s: str) -> bool:
    """
    Check if a string represents a valid signed integer.

    Args:
        s: String to check

    Returns:
        True if string is a valid signed integer, False otherwise
    """
    if not s:
        return False

    # Handle the case of a single minus sign
    if s == "-":
        return False

    # Check if it starts with one or more minus signs
    i = 0
    while i < len(s) and s[i] == "-":
        i += 1

    # If there's more than one minus sign at the beginning, it's invalid
    if i > 1:
        return False

    # The remaining part (after optional single minus sign) should all be digits
    remaining = s[i:]
    return remaining.isdigit()


def is_positive_integer(s: str) -> bool:
    """
    Check if a string represents a valid positive integer.

    Args:
        s: String to check

    Returns:
        True if string is a valid positive integer, False otherwise
    """
    return s.isdigit()


def is_in_range(
    value: Union[int, float], min_val: Union[int, float], max_val: Union[int, float]
) -> bool:
    """
    Check if a value is within an inclusive range [min_val, max_val].

    Args:
        value: Value to check
        min_val: Minimum value of range (inclusive)
        max_val: Maximum value of range (inclusive)

    Returns:
        True if value is in range, False otherwise
    """
    return min_val <= value <= max_val


def is_point_in_rect(
    px: Union[int, float],
    py: Union[int, float],
    rx: Union[int, float],
    ry: Union[int, float],
    rect_width: Union[int, float],
    rect_height: Union[int, float],
) -> bool:
    """
    Check if a point is within a rectangle (for hit detection).

    Args:
        px, py: Point coordinates
        rx, ry: Rectangle center coordinates
        rect_width: Rectangle width
        rect_height: Rectangle height

    Returns:
        True if point is inside rectangle, False otherwise
    """
    half_width = rect_width // 2
    half_height = rect_height // 2
    return abs(px - rx) <= half_width and abs(py - ry) <= half_height
