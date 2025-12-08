"""
Build script for creating executables with PyInstaller
"""

import subprocess
import sys
from pathlib import Path
import platform


def build_executable():
    """Build the executable using PyInstaller and the spec file."""

    system = platform.system().lower()

    # Run PyInstaller with the spec file
    print(f"Building executable for {system}...")

    # Create dist directory if it doesn't exist
    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)

    _ = subprocess.run([sys.executable, "-m", "PyInstaller", "build.spec"], check=True)

    print("Build completed successfully! Executable is in the 'dist' folder.")


if __name__ == "__main__":
    build_executable()
