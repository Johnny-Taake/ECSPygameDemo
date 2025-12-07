"""
Resource management utilities for bundled applications.
Handles asset paths for both development and executable environments.
"""

import os
import sys
from pathlib import Path


def get_resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource, works for dev and for PyInstaller.

    Args:
        relative_path: The relative path to the resource (e.g. 'assets/icon.png')

    Returns:
        The absolute path to the resource as a string
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS  # type: ignore
    except Exception:
        # If running in development, use the project root
        base_path = Path(__file__).parent.parent

    return os.path.join(base_path, relative_path)


def resource_exists(relative_path: str) -> bool:
    """
    Check if a resource exists at the given relative path.

    Args:
        relative_path: The relative path to check

    Returns:
        True if the resource exists, False otherwise
    """
    resource_path = get_resource_path(relative_path)
    return Path(resource_path).exists()


__all__ = ["get_resource_path", "resource_exists"]
