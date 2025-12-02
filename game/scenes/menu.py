import logging
from engine import BaseScene
from game.ui_builder import UIBuilder


log = logging.getLogger("game/scenes")


class MenuScene(BaseScene):
    def enter(self):
        log.info("MenuScene enter")
        ui = UIBuilder(self.app.font)
        self.title = ui.label_entity("Guess The Number", 300, 80)
        self.subtitle = ui.label_entity("Press Start", 300, 130, (200, 200, 200))

        def start_game():
            log.info("Start pressed")
            # Import here to avoid circular imports
            from .game import GameScene
            self.app.scene_manager.change(GameScene(self.app))

        self.btn_start = ui.button_entity("Start", 300, 240, start_game)

        def exit_game():
            log.info("Exit pressed")
            self.app.running = False

        self.btn_exit = ui.button_entity("EXIT", 300, 300, exit_game)

        self.entities = [self.title, self.subtitle, self.btn_start, self.btn_exit]

    def handle_event(self, event):
        # mouse clicks routed by InputSystem
        pass