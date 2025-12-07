from config import GameConfig


class LabelComponent:
    def __init__(self, text: str, color=GameConfig.LABEL_DEFAULT_COLOR):
        self.text: str = text
        self.color: tuple = color
