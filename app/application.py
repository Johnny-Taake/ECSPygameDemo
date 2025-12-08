import pygame

from config import GameConfig
from engine import InputSystem, RenderSystem, SoundSystem, SceneManager, ServiceLocator
from game import BootScene
from logger import get_logger
from utils import load_font_with_fallback
from utils.resources import get_resource_path
from utils.responsive import ResponsiveScaleManager

log = get_logger("main")


class GameApp:
    def __init__(
        self,
        width=GameConfig.WINDOW_WIDTH,
        height=GameConfig.WINDOW_HEIGHT,
        fps=GameConfig.FPS,
    ):
        pygame.init()

        # Set the icon
        icon_path = get_resource_path("assets/icon.png")
        icon = pygame.image.load(icon_path)
        pygame.display.set_caption(GameConfig.WINDOW_TITLE)

        # Initialize screen with RESIZABLE flag
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

        pygame.display.set_icon(icon)

        self.clock = pygame.time.Clock()
        self.fps = fps

        # Create virtual surface for fixed aspect ratio rendering
        self.virtual_surface = pygame.Surface(
            (GameConfig.WINDOW_WIDTH, GameConfig.WINDOW_HEIGHT)
        )

        # Create and configure scale manager
        self.scale_manager = ResponsiveScaleManager(
            base_width=GameConfig.WINDOW_WIDTH, base_height=GameConfig.WINDOW_HEIGHT
        )
        self.scale_manager.update_window_size(width, height)

        # Load custom font from file, fallback to system font if file is not available
        self.font = load_font_with_fallback(GameConfig.DEFAULT_FONT_SIZE)

        self.running = True

        # Initialize render system with virtual surface instead of screen
        self.render_system = RenderSystem(self.virtual_surface, self.font)
        self.input_system = InputSystem()
        self.sound_system = SoundSystem()

        self.scene_manager = SceneManager(self)
        self.scene_manager.change(BootScene(self))

        ServiceLocator.provide("app", self)
        ServiceLocator.provide("sound_system", self.sound_system)

    def run(self):
        while self.running:
            delta_time = self.clock.tick(self.fps) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

                # Handle window resize events
                if event.type == pygame.VIDEORESIZE:
                    log.debug(f"Window resized to: {event.w}x{event.h}")
                    self.screen = pygame.display.set_mode(
                        (event.w, event.h), pygame.RESIZABLE
                    )
                    self.scale_manager.update_window_size(event.w, event.h)
                    log.debug(f"Scale factor updated to: {self.scale_manager.scale}")
                    log.debug(
                        f"Offset calculated as: ({self.scale_manager.offset_x}, {self.scale_manager.offset_y})"
                    )

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Convert screen coordinates to virtual coordinates before processing
                    vx, vy = self.scale_manager.screen_to_world(*event.pos)
                    if self.scene_manager.current:
                        self.input_system.handle_mouse_down(
                            vx, vy, self.scene_manager.current.entities
                        )
                    # Process sound system for clicked buttons
                    if self.scene_manager.current:
                        self.sound_system.update(self.scene_manager.current.entities)

                if event.type == pygame.MOUSEBUTTONUP:
                    # Convert screen coordinates to virtual coordinates before processing
                    vx, vy = self.scale_manager.screen_to_world(*event.pos)
                    if self.scene_manager.current:
                        self.input_system.handle_mouse_up(
                            vx, vy, self.scene_manager.current.entities
                        )
                    # Process sound system for clicked buttons
                    if self.scene_manager.current:
                        self.sound_system.update(self.scene_manager.current.entities)

                if event.type == pygame.MOUSEMOTION:
                    # Convert screen coordinates to virtual coordinates before processing
                    vx, vy = self.scale_manager.screen_to_world(*event.pos)
                    if self.scene_manager.current:
                        self.input_system.handle_mouse_motion(
                            vx, vy, self.scene_manager.current.entities
                        )

                if event.type == pygame.KEYDOWN:
                    # Handle global sound toggle (Ctrl+M) - works in all scenes
                    if event.key == pygame.K_m and (event.mod & pygame.KMOD_CTRL):
                        if self.sound_system:
                            was_enabled = self.sound_system.enabled
                            if self.sound_system.enabled:
                                self.sound_system.disable_sounds()
                            else:
                                self.sound_system.enable_sounds()

                            # Play button click sound if sound was just enabled
                            if not was_enabled and self.sound_system.enabled:
                                self.sound_system.play_sound("button_click")

                            # Update the sound button image (safe to call on any scene)
                            if self.scene_manager.current:
                                self.scene_manager.current.update_sound_button_image(
                                    self.sound_system.enabled
                                )
                    else:
                        # Handle other keyboard events
                        self.input_system.handle_key(event)
                        if self.scene_manager.current:
                            self.scene_manager.current.handle_event(event)

            if self.scene_manager.current:
                try:
                    self.scene_manager.current.update(delta_time)
                except Exception as e:
                    log.exception("Scene update error: %s", e)

            # Process sound system for any entities with sound components
            if self.scene_manager.current:
                self.sound_system.update(self.scene_manager.current.entities)

            # Render to virtual surface first
            self.virtual_surface.fill(GameConfig.BACKGROUND_COLOR)
            if self.scene_manager.current:
                try:
                    self.render_system.update(self.scene_manager.current.entities)
                except Exception as e:
                    log.exception("Render error: %s", e)

            # Scale and blit virtual surface to actual screen with letterboxing
            self.screen.fill(
                (30, 30, 30)
            )  # Letterbox background (same as BACKGROUND_COLOR)

            # Calculate scaled dimensions
            scaled_width = int(
                self.virtual_surface.get_width() * self.scale_manager.scale
            )
            scaled_height = int(
                self.virtual_surface.get_height() * self.scale_manager.scale
            )

            # Scale the virtual surface
            scaled_surface = pygame.transform.scale(
                self.virtual_surface, (scaled_width, scaled_height)
            )

            # Blit scaled surface to screen with offset for centering
            self.screen.blit(
                scaled_surface,
                (self.scale_manager.offset_x, self.scale_manager.offset_y),
            )

            pygame.display.flip()

        pygame.quit()
        log.info("GameApp terminated")
