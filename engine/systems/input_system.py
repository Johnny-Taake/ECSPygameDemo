from pygame.event import Event

from engine.components import Position, ButtonComponent, InputFieldComponent


class InputSystem:
    def __init__(self):
        self.focused_input = None

    def set_focus(self, input_component: InputFieldComponent):
        if self.focused_input:
            self.focused_input.focused = False
        self.focused_input = input_component
        if input_component:
            input_component.focused = True

    def handle_key(self, key_event: Event):
        from pygame import K_BACKSPACE, K_RETURN

        if not self.focused_input:
            return
        if key_event.key == K_BACKSPACE:
            self.focused_input.text = self.focused_input.text[:-1]
        elif key_event.key == K_RETURN:
            # handled by scenes / buttons via events
            pass
        else:
            ch = key_event.unicode
            if ch.isprintable() and (
                len(self.focused_input.text) < self.focused_input.max_length
            ):
                self.focused_input.text += ch

    def handle_mouse(self, mx, my, entities):
        # click detection: if click in input area -> focus it
        for e in entities:
            pos = e.get(Position)
            btn = e.get(ButtonComponent)
            inp = e.get(InputFieldComponent)
            if not pos:
                continue
            if btn:
                # Use actual button dimensions for click detection
                half_width = btn.width // 2
                half_height = btn.height // 2
                if abs(mx - pos.x) <= half_width and abs(my - pos.y) <= half_height:
                    if (
                        btn.on_click and btn.active
                    ):  # Only respond to clicks if the button is active
                        btn.on_click()
            if inp:
                if abs(mx - pos.x) <= 120 and abs(my - pos.y) <= 20:
                    self.set_focus(inp)

    def handle_mouse_motion(self, mx, my, entities):
        # reset all button hover states first
        for e in entities:
            btn = e.get(ButtonComponent)
            if btn:
                btn.hover = False

        # check which buttons are being hovered over
        for e in entities:
            pos = e.get(Position)
            btn = e.get(ButtonComponent)
            if not pos or not btn:
                continue
            # Use actual button dimensions to detect hover
            half_width = btn.width // 2
            half_height = btn.height // 2
            if abs(mx - pos.x) <= half_width and abs(my - pos.y) <= half_height:
                btn.hover = True
