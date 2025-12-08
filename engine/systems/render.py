import pygame
from pygame import Rect, draw
from pygame.font import Font
from pygame.surface import Surface

from config import GameConfig
from utils import (
    apply_alpha,
    scale_text_to_width,
    load_font_with_fallback,
    load_image_with_fallback,
)
from logger import get_logger

from ..components import (
    AlphaComponent,
    ButtonComponent,
    H1Component,
    H2Component,
    H3Component,
    ImageComponent,
    InputFieldComponent,
    LabelComponent,
    Position,
    ProgressBarComponent,
)

log = get_logger("engine/render_system")


class RenderSystem:
    def __init__(self, screen: Surface, font: Font):
        self.screen = screen
        self.font = font
        # Load custom fonts from file paths for headers, fallback to system if custom fails
        self.h1_font = load_font_with_fallback(GameConfig.H1_FONT_SIZE)
        self.h2_font = load_font_with_fallback(GameConfig.H2_FONT_SIZE)
        self.h3_font = load_font_with_fallback(GameConfig.H3_FONT_SIZE)
        self.shortcut_font = load_font_with_fallback(GameConfig.BUTTON_TAG_FONT_SIZE)

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
        from config import GameConfig

        surf = self.h1_font.render(h1.text, True, h1.color)

        # Check if the text is too wide for the screen and scale if necessary
        max_width = (
            GameConfig.TEXT_MAX_WIDTH
        )  # Maximum width for H1 text (less than full screen width)
        surf = scale_text_to_width(surf, max_width)

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
        from config import GameConfig

        surf = self.h2_font.render(h2.text, True, h2.color)

        # Check if the text is too wide for the screen and scale if necessary
        max_width = GameConfig.TEXT_MAX_WIDTH
        surf = scale_text_to_width(surf, max_width)

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
        from config import GameConfig

        surf = self.h3_font.render(h3.text, True, h3.color)

        # Check if the text is too wide for the screen and scale if necessary
        max_width = GameConfig.TEXT_MAX_WIDTH
        surf = scale_text_to_width(surf, max_width)

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

        large_font = pygame.font.SysFont(
            GameConfig.DEFAULT_FONT, GameConfig.INPUT_FIELD_FONT_SIZE
        )
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

        input_width = GameConfig.INPUT_FIELD_WIDTH
        draw.line(
            self.screen,
            GameConfig.INPUT_UNDERLINE_COLOR,
            (position.x - input_width, underline_y),
            (position.x + input_width, underline_y),
            4,
        )

    def draw_button(
        self, button: ButtonComponent, position: Position, alpha: float = 1.0
    ):
        # Muted color when inactive
        color = (
            GameConfig.ACTIVE_BUTTON_TEXT_COLOR
            if button.active
            else GameConfig.INACTIVE_BUTTON_GRAYED_COLOR
        )

        # Handle text rendering
        if button.text:
            surf = self.font.render(button.text, True, color)
        else:
            surf = pygame.Surface((1, 1), pygame.SRCALPHA)

        # Apply transparency if alpha is less than 1.0
        if alpha < 1.0:
            temp_surf = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
            temp_surf.blit(surf, (0, 0))
            temp_surf.fill(
                (255, 255, 255, int(255 * alpha)), special_flags=pygame.BLEND_RGBA_MULT
            )
            surf = temp_surf

        text_rect = surf.get_rect(center=(position.x, position.y))
        pad = GameConfig.BUTTON_PADDING

        # Sizes of the button
        text_width = text_rect.width + pad * 2
        text_height = text_rect.height + pad * 2
        box_width = max(text_width, button.min_width)
        box_height = max(text_height, button.min_height)

        # Offset for button press animation
        press_offset = 2 if getattr(button, "pressed", False) and button.active else 0

        box = Rect(
            position.x - box_width // 2,
            position.y - box_height // 2 + press_offset,
            box_width,
            box_height,
        )

        if not button.active:
            bg_color = GameConfig.INACTIVE_BUTTON_BG_COLOR
        else:
            bg_color = (
                GameConfig.BUTTON_HOVER_COLOR
                if button.hover
                else GameConfig.BUTTON_BG_COLOR
            )

        shadow_color = tuple(max(c - 40, 0) for c in bg_color)

        if alpha < 1.0:
            bg_color = apply_alpha(bg_color, alpha)
            shadow_color = apply_alpha(shadow_color, alpha)

        # Shadow under the button (a bit lower)
        shadow_offset = 3
        shadow_rect = box.move(0, shadow_offset)
        draw.rect(
            self.screen,
            shadow_color,
            shadow_rect,
            border_radius=GameConfig.BUTTON_RADIUS,
        )

        # Main button box
        draw.rect(
            self.screen,
            bg_color,
            box,
            border_radius=GameConfig.BUTTON_RADIUS,
        )

        # Soft gradient highlight
        highlight_height = max(4, box.height // 2)  # top half of the button
        highlight_surf = pygame.Surface(
            (box.width - 4, highlight_height), pygame.SRCALPHA
        )

        # Draw a vertical gradient
        max_alpha = 70
        for y in range(highlight_height):
            t = y / highlight_height  # 0..1
            a = int(max_alpha * (1.0 - t))  # from max_alpha to 0
            pygame.draw.line(
                highlight_surf,
                (255, 255, 255, a),
                (0, y),
                (highlight_surf.get_width(), y),
            )

        self.screen.blit(
            highlight_surf,
            (box.left + 2, box.top + 2),
        )

        if button.text:
            text_rect = surf.get_rect(center=box.center)
            self.screen.blit(surf, text_rect)

        # Keyboard shortcut tag (как было)
        if button.keyboard_shortcut:
            shortcut_surf = self.shortcut_font.render(
                button.keyboard_shortcut, True, GameConfig.SHORTCUT_TAG_COLOR
            )
            shortcut_rect = shortcut_surf.get_rect()
            shortcut_x = box.right - shortcut_rect.width - 4
            shortcut_y = box.top + 2
            self.screen.blit(shortcut_surf, (shortcut_x, shortcut_y))

        # Store button dimensions for click detection
        button.width = box.width
        button.height = box.height

    def draw_progress_bar(
        self, progress_bar: ProgressBarComponent, position: Position, alpha: float = 1.0
    ):
        # Apply alpha to colors if needed
        if alpha < 1.0:
            bg_color = apply_alpha(progress_bar.color, alpha)
            fill_color = apply_alpha(progress_bar.fill_color, alpha)
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
            border_color = tuple(
                int(c * alpha) for c in GameConfig.PROGRESS_BAR_BORDER_COLOR
            )
        else:
            border_color = GameConfig.PROGRESS_BAR_BORDER_COLOR

        draw.rect(
            self.screen,
            border_color,
            bg_rect,
            2,
            border_radius=GameConfig.PROGRESS_BAR_BORDER_RADIUS,
        )

    def draw_image(self, image: ImageComponent, position: Position, alpha: float = 1.0):
        # Load the image if not already loaded
        if image.pygame_image is None:
            image.pygame_image = load_image_with_fallback(
                image.image_path, image.width or 40, image.height or 40
            )

        # Safety check: ensure image.pygame_image is not None before using it
        # This handles the edge case where something went wrong in the loading process
        if image.pygame_image is None:
            image.pygame_image = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.rect(
                image.pygame_image, (255, 0, 255), pygame.Rect(0, 0, 50, 50)
            )  # Magenta for error

        # Create a temporary surface for alpha transparency
        if alpha < 1.0:
            # Create a temporary surface with per-pixel alpha
            temp_surf = pygame.Surface(image.pygame_image.get_size(), pygame.SRCALPHA)
            temp_surf.blit(image.pygame_image, (0, 0))
            # Make it transparent
            temp_surf.fill(
                (255, 255, 255, int(255 * alpha)), special_flags=pygame.BLEND_RGBA_MULT
            )
            img = temp_surf
        else:
            img = image.pygame_image

        # Calculate position to center the image
        rect = img.get_rect(center=(position.x, position.y))
        self.screen.blit(img, rect)

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
                old_alpha = alpha_comp.alpha
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

                # Log transparency changes if significant
                if abs(alpha_comp.alpha - old_alpha) > 0.01:
                    log.debug(
                        f"Alpha component updated: {old_alpha:.3f} -> {alpha_comp.alpha:.3f}"
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
            img = e.get(ImageComponent)

            # If this entity has both button and image components, handle press animation together
            if btn and img:
                # Calculate press offset for the image to match button press animation
                press_offset = 2 if getattr(btn, "pressed", False) and btn.active else 0
                adjusted_pos = Position(pos.x, pos.y + press_offset)
                self.draw_button(
                    btn, pos, alpha
                )  # Button draws with its own internal offset
                self.draw_image(
                    img, adjusted_pos, alpha
                )  # Image drawn with matching offset
            else:
                if btn:
                    self.draw_button(btn, pos, alpha)
                if img:
                    self.draw_image(img, pos, alpha)
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
