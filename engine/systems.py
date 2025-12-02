import pygame
from pygame import draw, Rect, K_BACKSPACE, K_RETURN
from pygame.surface import Surface
from pygame.event import Event
from pygame.font import Font

from .components import (
    LabelComponent, Position, InputFieldComponent, ButtonComponent,
    H1Component, H2Component, H3Component
)
from config import GameConfig


class RenderSystem:
    def __init__(self, screen: Surface, font: Font):
        self.screen = screen
        self.font = font
        self.h1_font = pygame.font.SysFont(GameConfig.DEFAULT_FONT, 36)
        self.h2_font = pygame.font.SysFont(GameConfig.DEFAULT_FONT, 28)
        self.h3_font = pygame.font.SysFont(GameConfig.DEFAULT_FONT, 24)

    def draw_label(self, label: LabelComponent, position: Position):
        surf = self.font.render(label.text, True, label.color)
        rect = surf.get_rect(center=(position.x, position.y))
        self.screen.blit(surf, rect)

    def draw_h1(self, h1: H1Component, position: Position):
        surf = self.h1_font.render(h1.text, True, h1.color)
        rect = surf.get_rect(center=(position.x, position.y))
        self.screen.blit(surf, rect)

    def draw_h2(self, h2: H2Component, position: Position):
        surf = self.h2_font.render(h2.text, True, h2.color)
        rect = surf.get_rect(center=(position.x, position.y))
        self.screen.blit(surf, rect)

    def draw_h3(self, h3: H3Component, position: Position):
        surf = self.h3_font.render(h3.text, True, h3.color)
        rect = surf.get_rect(center=(position.x, position.y))
        self.screen.blit(surf, rect)

    def draw_input(self, inp: InputFieldComponent, position: Position):
        text = inp.text if inp.text else inp.placeholder
        text_color = GameConfig.TEXT_COLOR if inp.text else GameConfig.HINT_COLOR[:3]

        large_font = pygame.font.SysFont(GameConfig.DEFAULT_FONT, 28)
        surf = large_font.render(f"> {text}", True, text_color)
        rect = surf.get_rect(center=(position.x, position.y))
        self.screen.blit(surf, rect)

        underline_y = position.y + int(large_font.get_linesize() / 1.8)

        input_width = 280
        draw.line(
            self.screen,
            (100, 100, 100),
            (position.x - input_width, underline_y),
            (position.x + input_width, underline_y),
            4,
        )

    def draw_button(self, button: ButtonComponent, position: Position):
        # Muted color when inactive
        color = (0, 0, 0) if button.active else (100, 100, 100)
        surf = self.font.render(button.text, True, color)
        rect = surf.get_rect(center=(position.x, position.y))
        pad = GameConfig.BUTTON_PADDING

        # Calculate box width: use the larger of text width or min_width
        text_width = rect.width + pad * 2
        box_width = max(text_width, button.min_width)
        box = Rect(
            position.x - box_width // 2, rect.y - pad, box_width, rect.height + pad * 2
        )

        # TODO: Move the muted color to config
        if not button.active:
            color = (150, 150, 150)
        else:
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

            h1 = e.get(H1Component)
            if h1:
                self.draw_h1(h1, pos)
            h2 = e.get(H2Component)
            if h2:
                self.draw_h2(h2, pos)
            h3 = e.get(H3Component)
            if h3:
                self.draw_h3(h3, pos)

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
                    if btn.on_click and btn.active:  # Only respond to clicks if the button is active
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
