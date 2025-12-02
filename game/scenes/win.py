import logging
from engine import BaseScene, ButtonComponent, UIBuilder, AlphaComponent
from config import GameConfig


log = logging.getLogger("game/scenes")


class WinScene(BaseScene):
    def __init__(self, app, attempts: int):
        super().__init__(app)
        self.attempts = attempts
        self._next_scene = None
        self._fading_out = False

    def enter(self):
        log.info("WinScene enter")
        ui = UIBuilder(self.app.font)

        self.title = ui.h1_entity("Correct!", 300, 100, GameConfig.SUCCESS_COLOR)
        self.stat = ui.h2_entity(
            f"Attempts: {self.attempts}", 300, 160, GameConfig.HINT_COLOR
        )

        # def play_again():
        #     log.info("Play again")
        #     from .game import GameScene
        #     self.app.scene_manager.change(GameScene(self.app))

        def to_menu():
            # Start fade out before changing scene
            self.start_fade_out()

        def start_play_again():
            # For play again, we can also add fade transition if desired
            log.info("Play again")
            from .game import GameScene
            # Start fade out before changing scene
            self._next_scene = GameScene(self.app)
            self.start_fade_out()
            # The actual scene change will happen after fade completes

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
        # Handle fade out if needed
        if hasattr(self, '_fading_out') and self._fading_out:
            # Check if all entities have faded out (current alpha is at or near target alpha of 0)
            all_faded = True
            for entity in self.entities:
                alpha_comp = entity.get(AlphaComponent)
                if alpha_comp:
                    # Check if alpha is still above a very small threshold (close enough to 0)
                    if alpha_comp.alpha > 0.01:  # Still visible, not fully faded
                        all_faded = False
                        break

            # If all entities are fully transparent, transition to the appropriate scene
            if all_faded:
                if hasattr(self, '_next_scene') and self._next_scene is not None:
                    self.app.scene_manager.change(self._next_scene)
                else:
                    from .menu import MenuScene
                    self.app.scene_manager.change(MenuScene(self.app))

    def start_fade_out(self):
        """Start the fade out animation before transitioning to the next scene"""
        self._fading_out = True
        for entity in self.entities:
            alpha_comp = entity.get(AlphaComponent)
            if alpha_comp:
                alpha_comp.target_alpha = 0.0  # Fade to transparent
