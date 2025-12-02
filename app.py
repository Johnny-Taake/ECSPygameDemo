import logging
import pygame

from engine import RenderSystem, InputSystem, SceneManager, ServiceLocator
from game import BootScene

# Configure logging to show all messages
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

log = logging.getLogger("main")


class GameApp:
    def __init__(self, width=640, height=400, fps=60):
        pygame.init()

        # Set the icon
        icon = pygame.image.load("assets/icon.png")
        pygame.display.set_caption("Guess The Number")

        self.screen = pygame.display.set_mode((width, height))

        # Set the application ID for Windows taskbar icon
        import os
        if os.name == 'nt':  # Windows
            import ctypes
            myappid = 'com.guessnumber.game'  # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        # Set the icon after window creation for better compatibility
        pygame.display.set_icon(icon)

        self.clock = pygame.time.Clock()
        self.fps = fps
        self.font = pygame.font.SysFont('arial', 18)
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
            self.screen.fill((30, 30, 30))
            if self.scene_manager.current:
                try:
                    self.render_system.update(
                        self.scene_manager.current.entities)
                except Exception as e:
                    log.exception("Render error: %s", e)

            pygame.display.flip()

        pygame.quit()
        log.info("GameApp terminated")
