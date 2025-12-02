import logging
from engine import BaseScene, ButtonComponent, UIBuilder
from config import GameConfig


log = logging.getLogger("game/scenes")


class WinScene(BaseScene):
    def __init__(self, app, attempts: int):
        super().__init__(app)
        self.attempts = attempts

    def enter(self):
        log.info("WinScene enter")
        ui = UIBuilder(self.app.font)

        self.title = ui.h1_entity("Correct!", 300, 100, GameConfig.SUCCESS_COLOR)
        self.stat = ui.h2_entity(
            f"Attempts: {self.attempts}", 300, 160, GameConfig.HINT_COLOR
        )

        def play_again():
            log.info("Play again")
            from .game import GameScene
            self.app.scene_manager.change(GameScene(self.app))

        def menu():
            log.info("To menu")
            from .menu import MenuScene
            self.app.scene_manager.change(MenuScene(self.app))

        self.btn_play = ui.button_entity("Play Again", 300, 250, play_again)
        # Set minimum width to match longest button text in scene
        play_component = self.btn_play.get(ButtonComponent)
        if play_component:
            play_component.min_width = 140  # Fixed width for uniform buttons

        self.btn_menu = ui.button_entity("Menu", 300, 310, menu)
        # Set minimum width to match longest button text in scene
        menu_component = self.btn_menu.get(ButtonComponent)
        if menu_component:
            menu_component.min_width = 140  # Fixed width for uniform buttons

        self.entities = [self.title, self.stat, self.btn_play, self.btn_menu]
