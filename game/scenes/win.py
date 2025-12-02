import logging
from engine import BaseScene, LabelComponent
from game.ui_builder import UIBuilder
from config import GameConfig


log = logging.getLogger("game/scenes")


class WinScene(BaseScene):
    def __init__(self, app, attempts: int):
        super().__init__(app)
        self.attempts = attempts

    def enter(self):
        log.info("WinScene enter")
        ui = UIBuilder(self.app.font)

        self.title = ui.label_entity("Correct!", 300, 100, GameConfig.SUCCESS_COLOR)
        self.stat = ui.label_entity(
            f"Attempts: {self.attempts}", 300, 160, GameConfig.HINT_COLOR
        )

        def play_again():
            log.info("Play again")
            # Import here to avoid circular imports
            from .game import GameScene
            self.app.scene_manager.change(GameScene(self.app))

        def menu():
            log.info("To menu")
            # Import here to avoid circular imports
            from .menu import MenuScene
            self.app.scene_manager.change(MenuScene(self.app))

        self.btn_play = ui.button_entity("Play Again", 300, 250, play_again)
        self.btn_menu = ui.button_entity("Menu", 300, 310, menu)

        self.entities = [self.title, self.stat, self.btn_play, self.btn_menu]