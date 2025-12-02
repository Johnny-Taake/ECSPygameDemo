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
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.fill_color = fill_color
        self.progress = 0  # 0.0 to 1.0
        self.target_progress = 0  # 0.0 to 1.0
        self.animation_speed = (
            GameConfig.PROGRESS_BAR_ANIMATION_SPEED
        )  # How fast the progress fills visually
