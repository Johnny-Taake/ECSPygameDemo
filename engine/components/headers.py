from config import GameConfig


class H1Component:
    def __init__(self, text: str, color=GameConfig.H1_DEFAULT_COLOR):
        self.text: str = text
        self.color: tuple = color
        self.size: int = GameConfig.H1_FONT_SIZE


class H2Component:
    def __init__(self, text: str, color=GameConfig.H2_DEFAULT_COLOR):
        self.text: str = text
        self.color: tuple = color
        self.size: int = GameConfig.H2_FONT_SIZE


class H3Component:
    def __init__(self, text: str, color=GameConfig.H3_DEFAULT_COLOR):
        self.text: str = text
        self.color: tuple = color
        self.size: int = GameConfig.H3_FONT_SIZE
