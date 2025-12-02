class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class LabelComponent:
    def __init__(self, text: str, color=(255, 255, 255)):
        self.text = text
        self.color = color


class H1Component:
    def __init__(self, text: str, color=(255, 255, 255)):
        self.text = text
        self.color = color
        self.size = 36


class H2Component:
    def __init__(self, text: str, color=(255, 255, 255)):
        self.text = text
        self.color = color
        self.size = 28


class H3Component:
    def __init__(self, text: str, color=(255, 255, 255)):
        self.text = text
        self.color = color
        self.size = 24


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
        self.active = True
        self.width = 0
        self.height = 0
        self.min_width = 0


class ProgressBarComponent:
    def __init__(self, x: int, y: int, width: int, height: int, color=(100, 100, 100), fill_color=(0, 200, 0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.fill_color = fill_color
        self.progress = 0  # 0.0 to 1.0
        self.target_progress = 0  # 0.0 to 1.0
        self.animation_speed = 8.0  # How fast the progress fills visually


class AlphaComponent:
    def __init__(self, alpha: float = 1.0):
        """
        Alpha component for transparency
        :param alpha: 0.0 (fully transparent) to 1.0 (fully opaque)
        """
        self.alpha = alpha  # 0.0 (transparent) to 1.0 (opaque)
        self.target_alpha = alpha  # Target alpha for smooth transitions
        self.animation_speed = 3.0  # How fast alpha changes - faster for more immediate response
