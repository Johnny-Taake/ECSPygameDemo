from pygame.event import Event

from config import GameConfig
from engine.components import ButtonComponent, InputFieldComponent, Position


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
        self.handle_mouse_down(mx, my, entities)

    def handle_mouse_down(self, mx, my, entities):
        """Handle mouse button DOWN event."""
        for e in entities:
            pos = e.get(Position)
            btn = e.get(ButtonComponent)
            inp = e.get(InputFieldComponent)
            if not pos:
                continue

            if btn:
                from engine.components import ImageComponent
                img_component = e.get(ImageComponent)

                half_width = btn.width // 2
                half_height = btn.height // 2

                # Larger click area for image buttons
                if img_component:
                    min_click_width = 40
                    min_click_height = 40
                    half_width = max(half_width, min_click_width // 2)
                    half_height = max(half_height, min_click_height // 2)

                if abs(mx - pos.x) <= half_width and abs(my - pos.y) <= half_height:
                    if btn.active:
                        # Only set pressed state, do NOT trigger click yet
                        btn.pressed = True

            # Focus input field
            if inp:
                if (
                    abs(mx - pos.x) <= GameConfig.INPUT_MOUSE_DETECTION_WIDTH
                    and abs(my - pos.y) <= GameConfig.INPUT_MOUSE_DETECTION_HEIGHT
                ):
                    self.set_focus(inp)

    def handle_mouse_up(self, mx, my, entities):
        """Handle mouse button UP event."""
        for e in entities:
            pos = e.get(Position)
            btn = e.get(ButtonComponent)
            if not pos or not btn:
                continue

            # Only check buttons that were pressed
            if btn.pressed:
                half_width = btn.width // 2
                half_height = btn.height // 2

                # If cursor still over the button = valid click
                if abs(mx - pos.x) <= half_width and abs(my - pos.y) <= half_height:
                    if btn.on_click and btn.active:
                        btn.on_click()

                # Reset pressed state regardless
                btn.pressed = False

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
