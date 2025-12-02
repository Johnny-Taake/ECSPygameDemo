from config import GameConfig


class InputFieldComponent:
    def __init__(self, max_length: int = GameConfig.INPUT_FIELD_DEFAULT_MAX_LENGTH):
        self.text = ""
        self.max_length = max_length
        self.focused = False
        self.placeholder = ""

    def clear(self):
        self.text = ""
