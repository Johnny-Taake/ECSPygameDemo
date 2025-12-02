import pygame
from pygame import draw, Rect
from pygame.surface import Surface
from pygame.font import Font

from ..components import (
    LabelComponent,
    Position,
    InputFieldComponent,
    ButtonComponent,
    H1Component,
    H2Component,
    H3Component,
    ProgressBarComponent,
    AlphaComponent,
)
from config import GameConfig


class RenderSystem:
    def __init__(self, screen: Surface, font: Font):
        self.screen = screen
        self.font = font
        self.h1_font = pygame.font.SysFont(GameConfig.DEFAULT_FONT, 36)
        self.h2_font = pygame.font.SysFont(GameConfig.DEFAULT_FONT, 28)
        self.h3_font = pygame.font.SysFont(GameConfig.DEFAULT_FONT, 24)

    def draw_label(self, label: LabelComponent, position: Position, alpha: float = 1.0):
        surf = self.font.render(label.text, True, label.color)

        # Apply transparency if alpha is less than 1.0
        if alpha < 1.0:
            # Create a temporary surface with per-pixel alpha
            temp_surf = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
            temp_surf.blit(surf, (0, 0))
            # Make it transparent
            temp_surf.fill(
                (255, 255, 255, int(255 * alpha)), special_flags=pygame.BLEND_RGBA_MULT
            )
            surf = temp_surf

        rect = surf.get_rect(center=(position.x, position.y))
        self.screen.blit(surf, rect)

    def draw_h1(self, h1: H1Component, position: Position, alpha: float = 1.0):
        surf = self.h1_font.render(h1.text, True, h1.color)

        # Apply transparency if alpha is less than 1.0
        if alpha < 1.0:
            # Create a temporary surface with per-pixel alpha
            temp_surf = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
            temp_surf.blit(surf, (0, 0))
            # Make it transparent
            temp_surf.fill(
                (255, 255, 255, int(255 * alpha)), special_flags=pygame.BLEND_RGBA_MULT
            )
            surf = temp_surf

        rect = surf.get_rect(center=(position.x, position.y))
        self.screen.blit(surf, rect)

    def draw_h2(self, h2: H2Component, position: Position, alpha: float = 1.0):
        surf = self.h2_font.render(h2.text, True, h2.color)

        # Apply transparency if alpha is less than 1.0
        if alpha < 1.0:
            # Create a temporary surface with per-pixel alpha
            temp_surf = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
            temp_surf.blit(surf, (0, 0))
            # Make it transparent
            temp_surf.fill(
                (255, 255, 255, int(255 * alpha)), special_flags=pygame.BLEND_RGBA_MULT
            )
            surf = temp_surf

        rect = surf.get_rect(center=(position.x, position.y))
        self.screen.blit(surf, rect)

    def draw_h3(self, h3: H3Component, position: Position, alpha: float = 1.0):
        surf = self.h3_font.render(h3.text, True, h3.color)

        # Apply transparency if alpha is less than 1.0
        if alpha < 1.0:
            # Create a temporary surface with per-pixel alpha
            temp_surf = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
            temp_surf.blit(surf, (0, 0))
            # Make it transparent
            temp_surf.fill(
                (255, 255, 255, int(255 * alpha)), special_flags=pygame.BLEND_RGBA_MULT
            )
            surf = temp_surf

        rect = surf.get_rect(center=(position.x, position.y))
        self.screen.blit(surf, rect)

    def draw_input(
        self, inp: InputFieldComponent, position: Position, alpha: float = 1.0
    ):
        text = inp.text if inp.text else inp.placeholder
        text_color = GameConfig.TEXT_COLOR if inp.text else GameConfig.HINT_COLOR[:3]

        large_font = pygame.font.SysFont(GameConfig.DEFAULT_FONT, 28)
        surf = large_font.render(f"> {text}", True, text_color)

        # Apply transparency if alpha is less than 1.0
        if alpha < 1.0:
            # Create a temporary surface with per-pixel alpha
            temp_surf = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
            temp_surf.blit(surf, (0, 0))
            # Make it transparent
            temp_surf.fill(
                (255, 255, 255, int(255 * alpha)), special_flags=pygame.BLEND_RGBA_MULT
            )
            surf = temp_surf

        rect = surf.get_rect(center=(position.x, position.y))
        self.screen.blit(surf, rect)

        underline_y = position.y + int(large_font.get_linesize() / 1.8)

        input_width = 300
        draw.line(
            self.screen,
            (100, 100, 100),
            (position.x - input_width, underline_y),
            (position.x + input_width, underline_y),
            4,
        )

    def draw_button(
        self, button: ButtonComponent, position: Position, alpha: float = 1.0
    ):
        # Muted color when inactive
        color = (0, 0, 0) if button.active else (100, 100, 100)
        surf = self.font.render(button.text, True, color)

        # Apply transparency if alpha is less than 1.0
        if alpha < 1.0:
            # Create a temporary surface with per-pixel alpha
            temp_surf = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
            temp_surf.blit(surf, (0, 0))
            # Make it transparent
            temp_surf.fill(
                (255, 255, 255, int(255 * alpha)), special_flags=pygame.BLEND_RGBA_MULT
            )
            surf = temp_surf

        rect = surf.get_rect(center=(position.x, position.y))
        pad = GameConfig.BUTTON_PADDING

        # Calculate box width: use the larger of text width or min_width
        text_width = rect.width + pad * 2
        box_width = max(text_width, button.min_width)
        box = Rect(
            position.x - box_width // 2, rect.y - pad, box_width, rect.height + pad * 2
        )

        # Calculate button color based on hover state and alpha
        if not button.active:
            bg_color = (150, 150, 150)
        else:
            bg_color = (
                GameConfig.BUTTON_HOVER_COLOR
                if button.hover
                else GameConfig.BUTTON_BG_COLOR
            )

        # Apply alpha to the background color
        if alpha < 1.0:
            bg_color = tuple(int(c * alpha) for c in bg_color)

        # Draw rounded rectangle for border radius effect
        draw.rect(self.screen, bg_color, box, border_radius=GameConfig.BUTTON_RADIUS)
        # Center the text in the button
        text_rect = surf.get_rect(center=(position.x, position.y))
        self.screen.blit(surf, text_rect)

        # Store button dimensions for click detection
        button.width = box.width
        button.height = box.height

    def draw_progress_bar(
        self, progress_bar: ProgressBarComponent, position: Position, alpha: float = 1.0
    ):
        # Apply alpha to colors if needed
        if alpha < 1.0:
            bg_color = tuple(int(c * alpha) for c in progress_bar.color)
            fill_color = tuple(int(c * alpha) for c in progress_bar.fill_color)
        else:
            bg_color = progress_bar.color
            fill_color = progress_bar.fill_color

        # Draw the background
        bg_rect = Rect(
            progress_bar.x - progress_bar.width // 2,
            progress_bar.y - progress_bar.height // 2,
            progress_bar.width,
            progress_bar.height,
        )
        draw.rect(self.screen, bg_color, bg_rect)

        # Draw the filled portion
        fill_width = int(progress_bar.width * progress_bar.progress)
        if fill_width > 0:
            fill_rect = Rect(
                progress_bar.x - progress_bar.width // 2,
                progress_bar.y - progress_bar.height // 2,
                fill_width,
                progress_bar.height,
            )
            draw.rect(self.screen, fill_color, fill_rect)

        # Draw border (also affected by alpha)
        if alpha < 1.0:
            border_color = tuple(int(c * alpha) for c in (255, 255, 255))
        else:
            border_color = (255, 255, 255)

        draw.rect(self.screen, border_color, bg_rect, 2, border_radius=3)

    def update(self, entities: list):
        for e in entities:
            pos: Position = e.get(Position)
            if not pos:
                continue

            # Get alpha component if it exists
            alpha_comp = e.get(AlphaComponent)
            alpha = alpha_comp.alpha if alpha_comp else 1.0

            # Update alpha component if it exists (for smooth transitions)
            if alpha_comp:
                # Update alpha with smooth animation towards target
                if alpha_comp.alpha < alpha_comp.target_alpha:
                    alpha_comp.alpha = min(
                        alpha_comp.alpha + alpha_comp.animation_speed * 0.016,
                        alpha_comp.target_alpha,
                    )
                elif alpha_comp.alpha > alpha_comp.target_alpha:
                    alpha_comp.alpha = max(
                        alpha_comp.alpha - alpha_comp.animation_speed * 0.016,
                        alpha_comp.target_alpha,
                    )

            h1 = e.get(H1Component)
            if h1:
                self.draw_h1(h1, pos, alpha)
            h2 = e.get(H2Component)
            if h2:
                self.draw_h2(h2, pos, alpha)
            h3 = e.get(H3Component)
            if h3:
                self.draw_h3(h3, pos, alpha)

            label = e.get(LabelComponent)
            if label:
                self.draw_label(label, pos, alpha)
            inp = e.get(InputFieldComponent)
            if inp:
                self.draw_input(inp, pos, alpha)
            btn = e.get(ButtonComponent)
            if btn:
                self.draw_button(btn, pos, alpha)
            pb = e.get(ProgressBarComponent)
            if pb:
                # Update progress with smooth animation towards target
                if pb.progress < pb.target_progress:
                    pb.progress = min(
                        pb.progress + pb.animation_speed * 0.016, pb.target_progress
                    )  # 0.016 is roughly 60fps
                elif pb.progress > pb.target_progress:
                    pb.progress = max(
                        pb.progress - pb.animation_speed * 0.016, pb.target_progress
                    )

                self.draw_progress_bar(pb, pos, alpha)
