# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

# Get the project root directory
import os
PROJECT_ROOT = Path(os.path.abspath('.'))

# Game assets to include
assets = [
    (str(PROJECT_ROOT / "assets"), "assets"),
]

# Additional files to include
additional_files = assets

# Hidden imports (if any)
hiddenimports = [
    "utils.resources",
    "config",
    "config.game_config",
    "config.ui",
    "config.base",
    "config.logging",
    "config.stats",
    "config.settings",
    "engine",
    "engine.components",
    "engine.systems",
    "game",
    "game.logic",
    "game.scenes",
    "logger",
    "logger.colored_formatter",
    "pydantic",
    "pydantic_settings",
]

# Determine the appropriate icon based on the platform
icon_path = str(PROJECT_ROOT / "assets" / "icon.png")

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[str(PROJECT_ROOT)],
    binaries=[],
    datas=additional_files,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GuessTheNumberGame',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True for debugging, False for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
)