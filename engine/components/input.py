from config import GameConfig


class InputFieldComponent:
    def __init__(self, max_length: int = GameConfig.INPUT_FIELD_DEFAULT_MAX_LENGTH):
        self.text: str = ""
        self.max_length: int = max_length
        self.focused: bool = False
        self.placeholder: str = ""

    def clear(self):
        self.text: str = ""
