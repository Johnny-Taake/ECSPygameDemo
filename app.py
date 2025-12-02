import logging
import pygame
from config import GameConfig

from engine import RenderSystem, InputSystem, SceneManager, ServiceLocator
from game import BootScene


# Configure logging based on config
logging.basicConfig(
    level=GameConfig.LOG_LEVEL,
    format=GameConfig.LOG_FORMAT,
)

log = logging.getLogger("main")


class GameApp:
    def __init__(self, width=GameConfig.WINDOW_WIDTH, height=GameConfig.WINDOW_HEIGHT, fps=GameConfig.FPS):
        pygame.init()

        # Set the icon
        icon = pygame.image.load("assets/icon.png")
        pygame.display.set_caption(GameConfig.WINDOW_TITLE)

        self.screen = pygame.display.set_mode((width, height))

        pygame.display.set_icon(icon)

        self.clock = pygame.time.Clock()
        self.fps = fps
        self.font = pygame.font.SysFont(GameConfig.DEFAULT_FONT, GameConfig.DEFAULT_FONT_SIZE)
        self.running = True

        self.render_system = RenderSystem(self.screen, self.font)
        self.input_system = InputSystem()

        self.scene_manager = SceneManager(self)
        self.scene_manager.change(BootScene(self))

        ServiceLocator.provide("app", self)

    def run(self):
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    if self.scene_manager.current:
                        self.input_system.handle_mouse(
                            mx, my, self.scene_manager.current.entities)
                if event.type == pygame.KEYDOWN:
                    self.input_system.handle_key(event)
                    if self.scene_manager.current:
                        self.scene_manager.current.handle_event(event)

            if self.scene_manager.current:
                try:
                    self.scene_manager.current.update(dt)
                except Exception as e:
                    log.exception("Scene update error: %s", e)

            # Render
            self.screen.fill(GameConfig.BACKGROUND_COLOR)
            if self.scene_manager.current:
                try:
                    self.render_system.update(
                        self.scene_manager.current.entities)
                except Exception as e:
                    log.exception("Render error: %s", e)

            pygame.display.flip()

        pygame.quit()
        log.info("GameApp terminated")
