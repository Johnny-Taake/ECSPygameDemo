class InputFieldComponent:
    def __init__(self, max_length: int = 6):
        self.text = ""
        self.max_length = max_length
        self.focused = False
        self.placeholder = ""

    def clear(self):
        self.text = ""
