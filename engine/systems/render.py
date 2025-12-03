import pygame
from pygame import Rect, draw
from pygame.font import Font
from pygame.surface import Surface

from config import GameConfig

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


class RenderSystem:
    def __init__(self, screen: Surface, font: Font):
        self.screen = screen
        self.font = font  # This should already be the custom font loaded from file
        # Load custom fonts from file paths for headers, fallback to system if custom fails
        try:
            self.h1_font = pygame.font.Font(
                GameConfig.DEFAULT_FONT_PATH, GameConfig.H1_FONT_SIZE
            )
        except:
            self.h1_font = pygame.font.SysFont(
                GameConfig.DEFAULT_FONT, GameConfig.H1_FONT_SIZE
            )

        try:
            self.h2_font = pygame.font.Font(
                GameConfig.DEFAULT_FONT_PATH, GameConfig.H2_FONT_SIZE
            )
        except:
            self.h2_font = pygame.font.SysFont(
                GameConfig.DEFAULT_FONT, GameConfig.H2_FONT_SIZE
            )

        try:
            self.h3_font = pygame.font.Font(
                GameConfig.DEFAULT_FONT_PATH, GameConfig.H3_FONT_SIZE
            )
        except:
            self.h3_font = pygame.font.SysFont(
                GameConfig.DEFAULT_FONT, GameConfig.H3_FONT_SIZE
            )

        # Load font for keyboard shortcut tags
        try:
            self.shortcut_font = pygame.font.Font(
                GameConfig.DEFAULT_FONT_PATH, GameConfig.BUTTON_TAG_FONT_SIZE
            )
        except:
            self.shortcut_font = pygame.font.SysFont(
                GameConfig.DEFAULT_FONT, GameConfig.BUTTON_TAG_FONT_SIZE
            )

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

        # Check if the text is too wide for the screen and scale if necessary
        max_width = 600  # Maximum width for H1 text (less than full screen width)
        if surf.get_width() > max_width:
            # Scale the text surface down to fit within max_width
            aspect_ratio = surf.get_height() / surf.get_width()
            new_width = max_width
            new_height = int(new_width * aspect_ratio)
            surf = pygame.transform.smoothscale(surf, (new_width, new_height))

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

        # Check if the text is too wide for the screen and scale if necessary
        max_width = 600  # Maximum width for H2 text (less than full screen width)
        if surf.get_width() > max_width:
            # Scale the text surface down to fit within max_width
            aspect_ratio = surf.get_height() / surf.get_width()
            new_width = max_width
            new_height = int(new_width * aspect_ratio)
            surf = pygame.transform.smoothscale(surf, (new_width, new_height))

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

        # Check if the text is too wide for the screen and scale if necessary
        max_width = 600  # Maximum width for H3 text (less than full screen width)
        if surf.get_width() > max_width:
            # Scale the text surface down to fit within max_width
            aspect_ratio = surf.get_height() / surf.get_width()
            new_width = max_width
            new_height = int(new_width * aspect_ratio)
            surf = pygame.transform.smoothscale(surf, (new_width, new_height))

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
        if button.text:  # If there's text, render it normally
            surf = self.font.render(button.text, True, color)
        else:  # If no text (like for image buttons), create an empty surface
            # For image buttons with empty text, create a transparent surface
            surf = pygame.Surface((1, 1), pygame.SRCALPHA)  # Tiny transparent surface

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

        # Calculate box width and height: use the larger of text dimensions or min dimensions
        # For image buttons (empty text), we rely on min_width and min_height to determine the padding area
        text_width = rect.width + pad * 2
        text_height = rect.height + pad * 2
        box_width = max(text_width, button.min_width)
        box_height = max(text_height, button.min_height)
        box = Rect(
            position.x - box_width // 2,
            position.y - box_height // 2,
            box_width,
            box_height,
        )

        # Calculate button color based on hover state and alpha
        if not button.active:
            bg_color = GameConfig.INACTIVE_BUTTON_BG_COLOR
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
        # Center the text in the button (only if it's not an image button)
        if button.text:  # Only blit text if it exists
            text_rect = surf.get_rect(center=(position.x, position.y))
            self.screen.blit(surf, text_rect)

        # Draw keyboard shortcut tag if available
        if button.keyboard_shortcut:
            # Render the keyboard shortcut in small font with muted color for white backgrounds
            shortcut_surf = self.shortcut_font.render(
                button.keyboard_shortcut, True, GameConfig.SHORTCUT_TAG_COLOR
            )
            # Position it at the top right of the button
            shortcut_rect = shortcut_surf.get_rect()
            # Position the shortcut tag in the top right corner inside the button
            shortcut_x = (
                box.right - shortcut_rect.width - 4
            )  # 4px padding from right edge
            shortcut_y = box.top + 2  # 2px padding from top edge
            self.screen.blit(shortcut_surf, (shortcut_x, shortcut_y))

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
            try:
                loaded_image = pygame.image.load(image.image_path).convert_alpha()

                # Resize if dimensions are specified
                if image.width and image.height:
                    loaded_image = pygame.transform.scale(
                        loaded_image, (image.width, image.height)
                    )

                image.pygame_image = loaded_image
            except pygame.error:
                # Create a placeholder surface if image fails to load
                image.pygame_image = pygame.Surface((50, 50), pygame.SRCALPHA)
                # Draw a red rectangle to indicate missing image
                pygame.draw.rect(
                    image.pygame_image, (255, 0, 0), pygame.Rect(0, 0, 50, 50)
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
            img = e.get(ImageComponent)
            if img:
                self.draw_image(img, pos, alpha)
