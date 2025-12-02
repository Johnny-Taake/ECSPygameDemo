from engine import (
    Entity,
    Position,
    LabelComponent,
    InputFieldComponent,
    ButtonComponent,
)


class UIBuilder:
    def __init__(self, font):
        self.font = font

    def label_entity(self, text: str, x: int, y: int, color=(255, 255, 255)):
        e = Entity()
        e.add(Position(x, y)).add(LabelComponent(text, color))
        return e

    def input_entity(self, placeholder: str, x: int, y: int, max_len: int = 6):
        e = Entity()
        inp = InputFieldComponent(max_len)
        inp.placeholder = placeholder
        e.add(Position(x, y)).add(inp)
        return e

    def button_entity(self, text: str, x: int, y: int, onclick):
        e = Entity()
        btn = ButtonComponent(text)
        btn.on_click = onclick
        e.add(Position(x, y)).add(btn)
        return e
