from .ecs import GameObject
from .components import (
    Position,
    LabelComponent,
    H1Component,
    H2Component,
    H3Component,
    InputFieldComponent,
    ButtonComponent,
    ProgressBarComponent,
)


class UIBuilder:
    def __init__(self, font):
        self.font = font

    def label_entity(self, text: str, x: int, y: int, color=(255, 255, 255)):
        e = GameObject()
        e.add(Position(x, y)).add(LabelComponent(text, color))
        return e

    def input_entity(self, placeholder: str, x: int, y: int, max_len: int = 6):
        e = GameObject()
        inp = InputFieldComponent(max_len)
        inp.placeholder = placeholder
        e.add(Position(x, y)).add(inp)
        return e

    def button_entity(self, text: str, x: int, y: int, onclick):
        e = GameObject()
        btn = ButtonComponent(text)
        btn.on_click = onclick
        e.add(Position(x, y)).add(btn)
        return e

    def button_entity_with_min_width(self, text: str, x: int, y: int, onclick, min_width: int):
        e = GameObject()
        btn = ButtonComponent(text)
        btn.on_click = onclick
        btn.min_width = min_width
        e.add(Position(x, y)).add(btn)
        return e

    def h1_entity(self, text: str, x: int, y: int, color=(255, 255, 255)):
        e = GameObject()
        e.add(Position(x, y)).add(H1Component(text, color))
        return e

    def h2_entity(self, text: str, x: int, y: int, color=(255, 255, 255)):
        e = GameObject()
        e.add(Position(x, y)).add(H2Component(text, color))
        return e

    def h3_entity(self, text: str, x: int, y: int, color=(255, 255, 255)):
        e = GameObject()
        e.add(Position(x, y)).add(H3Component(text, color))
        return e

    def progress_bar_entity(self, x: int, y: int, width: int, height: int, color=(100, 100, 100), fill_color=(0, 200, 0)):
        e = GameObject()
        e.add(Position(x, y)).add(ProgressBarComponent(x, y, width, height, color, fill_color))
        return e
