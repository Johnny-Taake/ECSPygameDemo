from typing import Optional


class ButtonComponent:
    def __init__(self, text: str, keyboard_shortcut: Optional[str] = None):
        self.text = text
        self.on_click = None
        self.hover = False
        self.active = True
        self.width = 0
        self.height = 0
        self.min_width = 0
        self.min_height = 0

        # Optional keyboard shortcut tag to display
        self.keyboard_shortcut = keyboard_shortcut

        self.pressed: bool = False
