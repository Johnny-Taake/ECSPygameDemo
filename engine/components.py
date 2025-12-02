class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class LabelComponent:
    def __init__(self, text: str, color=(255, 255, 255)):
        self.text = text
        self.color = color


class InputFieldComponent:
    def __init__(self, max_length: int = 6):
        self.text = ""
        self.max_length = max_length
        self.focused = False
        self.placeholder = ""

    def clear(self):
        self.text = ""


class ButtonComponent:
    def __init__(self, text: str):
        self.text = text
        self.on_click = None
        self.hover = False
        self.width = 0
        self.height = 0
