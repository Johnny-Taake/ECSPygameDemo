import pygame

from config import GameConfig
from engine import InputSystem, RenderSystem, SoundSystem, SceneManager, ServiceLocator
from game import BootScene
from logger import get_logger
from utils.resources import get_resource_path

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

        self.screen = pygame.display.set_mode((width, height))

        pygame.display.set_icon(icon)

        self.clock = pygame.time.Clock()
        self.fps = fps

        # Load custom font from file, fallback to system font if file is not available
        try:
            font_path = get_resource_path(GameConfig.DEFAULT_FONT_PATH)
            self.font = pygame.font.Font(
                font_path, GameConfig.DEFAULT_FONT_SIZE
            )
        except:
            # Fallback to system font if custom font fails to load
            self.font = pygame.font.SysFont(
                GameConfig.DEFAULT_FONT, GameConfig.DEFAULT_FONT_SIZE
            )

        self.running = True

        self.render_system = RenderSystem(self.screen, self.font)
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

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    if self.scene_manager.current:
                        self.input_system.handle_mouse(
                            mx, my, self.scene_manager.current.entities
                        )
                    # Process sound system for clicked buttons
                    if self.scene_manager.current:
                        self.sound_system.update(self.scene_manager.current.entities)

                if event.type == pygame.MOUSEMOTION:
                    mx, my = event.pos
                    if self.scene_manager.current:
                        self.input_system.handle_mouse_motion(
                            mx, my, self.scene_manager.current.entities
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

            # Render
            self.screen.fill(GameConfig.BACKGROUND_COLOR)
            if self.scene_manager.current:
                try:
                    self.render_system.update(self.scene_manager.current.entities)
                except Exception as e:
                    log.exception("Render error: %s", e)

            pygame.display.flip()

        pygame.quit()
        log.info("GameApp terminated")
