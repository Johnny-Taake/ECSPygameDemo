class ButtonComponent:
    def __init__(self, text: str):
        self.text = text
        self.on_click = None
        self.hover = False
        self.active = True
        self.width = 0
        self.height = 0
        self.min_width = 0
