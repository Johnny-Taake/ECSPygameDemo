from typing import Tuple

from config import GameConfig


class ProgressBarComponent:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color=GameConfig.PROGRESS_BAR_BG_COLOR,
        fill_color=GameConfig.PROGRESS_BAR_FILL_COLOR,
    ):
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.color: Tuple[int, int, int] = color
        self.fill_color: Tuple[int, int, int] = fill_color
        self.progress: float = 0  # 0.0 to 1.0
        self.target_progress: float = 0  # 0.0 to 1.0
        self.animation_speed: float = (
            GameConfig.PROGRESS_BAR_ANIMATION_SPEED
        )  # How fast the progress fills visually
