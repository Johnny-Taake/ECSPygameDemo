from pygame import draw, Rect, K_BACKSPACE, K_RETURN
from pygame.surface import Surface
from pygame.event import Event
from pygame.font import Font

from .components import LabelComponent, Position, InputFieldComponent, ButtonComponent
from config import GameConfig


class RenderSystem:
    def __init__(self, screen: Surface, font: Font):
        self.screen = screen
        self.font = font

    def draw_label(self, label: LabelComponent, position: Position):
        surf = self.font.render(label.text, True, label.color)
        rect = surf.get_rect(center=(position.x, position.y))
        self.screen.blit(surf, rect)

    def draw_input(self, inp: InputFieldComponent, position: Position):
        text = inp.text if inp.text else inp.placeholder
        text_color = GameConfig.TEXT_COLOR if inp.text else GameConfig.HINT_COLOR[:3]
        surf = self.font.render(f">{text}", True, text_color)
        rect = surf.get_rect(center=(position.x, position.y))
        self.screen.blit(surf, rect)
        underline_y = position.y + int(self.font.get_linesize() / 1.8)
        # Make the input field visually larger
        input_width = 180  # Increased from 120
        draw.line(
            self.screen,
            (100, 100, 100),
            (position.x - input_width, underline_y),
            (position.x + input_width, underline_y),
            2,
        )

    def draw_button(self, button: ButtonComponent, position: Position):
        surf = self.font.render(button.text, True, (0, 0, 0))
        rect = surf.get_rect(center=(position.x, position.y))
        pad = GameConfig.BUTTON_PADDING

        # Calculate box width: use the larger of text width or min_width
        text_width = rect.width + pad * 2
        box_width = max(text_width, button.min_width)
        box = Rect(
            position.x - box_width // 2, rect.y - pad, box_width, rect.height + pad * 2
        )
        color = GameConfig.BUTTON_HOVER_COLOR if button.hover else GameConfig.BUTTON_BG_COLOR
        # Draw rounded rectangle for border radius effect
        draw.rect(self.screen, color, box, border_radius=GameConfig.BUTTON_RADIUS)
        # Center the text in the button
        text_rect = surf.get_rect(center=(position.x, position.y))
        self.screen.blit(surf, text_rect)

        # Store button dimensions for click detection
        button.width = box.width
        button.height = box.height

    def update(self, entities: list):
        for e in entities:
            pos: Position = e.get(Position)
            if not pos:
                continue
            label = e.get(LabelComponent)
            if label:
                self.draw_label(label, pos)
            inp = e.get(InputFieldComponent)
            if inp:
                self.draw_input(inp, pos)
            btn = e.get(ButtonComponent)
            if btn:
                self.draw_button(btn, pos)


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
                    if btn.on_click:
                        btn.on_click()
            if inp:
                if abs(mx - pos.x) <= 120 and abs(my - pos.y) <= 20:
                    self.set_focus(inp)
