class ProgressBarComponent:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color=(100, 100, 100),
        fill_color=(0, 200, 0),
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.fill_color = fill_color
        self.progress = 0  # 0.0 to 1.0
        self.target_progress = 0  # 0.0 to 1.0
        self.animation_speed = 8.0  # How fast the progress fills visually
