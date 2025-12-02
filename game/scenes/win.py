from config import GameConfig
from engine import AlphaComponent, BaseScene, ButtonComponent, UIBuilder
from logger import get_logger

log = get_logger("game/scenes")


class WinScene(BaseScene):
    def __init__(self, app, attempts: int, game_logic=None):
        super().__init__(app)
        self.attempts = attempts
        self.game_logic = game_logic  # Store game logic to access difficulty info

    def enter(self):
        log.info("WinScene enter")
        ui = UIBuilder(self.app.font)

        self.title = ui.h1_entity("Correct!", 300, 100, GameConfig.SUCCESS_COLOR)
        self.stat = ui.h2_entity(
            f"Attempts: {self.attempts}", 300, 160, GameConfig.HINT_COLOR
        )

        def to_menu():
            # Store the current difficulty in service locator before going to menu
            if self.game_logic is not None:
                from engine import ServiceLocator
                from config import GameConfig

                # Find the corresponding difficulty index to store
                config_difficulty_modes = GameConfig.DIFFICULTY_MODES
                matching_index = None
                for i, mode in enumerate(config_difficulty_modes):
                    if mode.min == self.game_logic.min_number and mode.max == self.game_logic.max_number:
                        matching_index = i
                        break

                if matching_index is not None:
                    ServiceLocator.provide("last_selected_difficulty", matching_index)

            # Start fade out with callback to go to menu
            def on_fade_complete():
                from .menu import MenuScene
                self.app.scene_manager.change(MenuScene(self.app))

            self.start_fade_out(on_complete_callback=on_fade_complete)

        def start_play_again():
            # For play again, we can also add fade transition if desired
            log.info("Play again")

            # Store the current difficulty in service locator for the new game
            if self.game_logic is not None:
                from engine import ServiceLocator
                from config import GameConfig

                # Find the corresponding difficulty index to store
                config_difficulty_modes = GameConfig.DIFFICULTY_MODES
                matching_index = None
                for i, mode in enumerate(config_difficulty_modes):
                    if mode.min == self.game_logic.min_number and mode.max == self.game_logic.max_number:
                        matching_index = i
                        break

                if matching_index is not None:
                    ServiceLocator.provide("last_selected_difficulty", matching_index)

            from .game import GameScene

            # Start fade out with callback to go to game scene
            def on_fade_complete():
                self.app.scene_manager.change(GameScene(self.app))

            self.start_fade_out(on_complete_callback=on_fade_complete)

        self.btn_play = ui.button_entity("Play Again", 300, 250, start_play_again)
        # Set minimum width to match longest button text in scene
        play_component = self.btn_play.get(ButtonComponent)
        if play_component:
            play_component.min_width = 140  # Fixed width for uniform buttons

        self.btn_menu = ui.button_entity("Menu", 300, 310, to_menu)
        # Set minimum width to match longest button text in scene
        menu_component = self.btn_menu.get(ButtonComponent)
        if menu_component:
            menu_component.min_width = 140  # Fixed width for uniform buttons

        # Add alpha components to enable fade transitions
        for entity in [self.title, self.stat, self.btn_play, self.btn_menu]:
            entity.add(AlphaComponent(1.0))

        self.entities = [self.title, self.stat, self.btn_play, self.btn_menu]

    def update(self, delta_time: float):
        # Call parent update to handle fade-out if in progress
        super().update(delta_time)  # This calls the BaseScene's update method which handles fade-out
