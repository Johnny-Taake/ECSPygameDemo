from config import GameConfig
from engine import BaseScene, ButtonComponent, UIBuilder
from logger import get_logger

log = get_logger("game/scenes")


class MenuScene(BaseScene):
    def enter(self):
        log.info("MenuScene enter")
        self._exit_requested = False
        self._fading_out = False
        ui = UIBuilder(self.app.font)
        self.title = ui.h1_entity("Guess The Number", 300, 80)
        self.subtitle = ui.h2_entity("Press START", 300, 130, GameConfig.HINT_COLOR)

        def start_game():
            log.info("Start pressed")
            # Start fade out with callback to start the game
            def on_fade_complete():
                from .game import GameScene
                self.app.scene_manager.change(GameScene(self.app))

            self.start_fade_out(on_complete_callback=on_fade_complete)

        self.btn_start = ui.button_entity("START", 300, 240, start_game)
        # Set minimum width to match longest button text in scene
        start_component = self.btn_start.get(ButtonComponent)
        if start_component:
            start_component.min_width = 140  # Fixed width for uniform buttons

        def exit_game():
            log.info("Exit pressed")
            # Start fade out with callback to exit the application
            def on_fade_complete():
                self.app.running = False

            self.start_fade_out(on_complete_callback=on_fade_complete)

        self.btn_exit = ui.button_entity("EXIT", 300, 300, exit_game)
        # Set minimum width to match longest button text in scene
        exit_component = self.btn_exit.get(ButtonComponent)
        if exit_component:
            exit_component.min_width = 140  # Fixed width for uniform buttons

        # Add alpha components to enable fade transitions
        from engine import AlphaComponent

        for entity in [self.title, self.subtitle, self.btn_start, self.btn_exit]:
            entity.add(AlphaComponent(1.0))

        self.entities = [self.title, self.subtitle, self.btn_start, self.btn_exit]

    def handle_event(self, event):
        # mouse clicks routed by InputSystem
        pass

    def update(self, delta_time: float):
        # Call parent update to handle fade-out if in progress
        super().update(delta_time)  # This calls the BaseScene's update method which handles fade-out
