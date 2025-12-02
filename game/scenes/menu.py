import logging
from engine import BaseScene, ButtonComponent, UIBuilder, AlphaComponent


log = logging.getLogger("game/scenes")


class MenuScene(BaseScene):
    def enter(self):
        log.info("MenuScene enter")
        self._exit_requested = False
        self._fading_out = False
        ui = UIBuilder(self.app.font)
        self.title = ui.h1_entity("Guess The Number", 300, 80)
        self.subtitle = ui.h2_entity("Press Start", 300, 130, (200, 200, 200))

        def start_game():
            log.info("Start pressed")
            # Start fade out before changing scene
            self.start_fade_out()

        self.btn_start = ui.button_entity("START", 300, 240, start_game)
        # Set minimum width to match longest button text in scene
        start_component = self.btn_start.get(ButtonComponent)
        if start_component:
            start_component.min_width = 140  # Fixed width for uniform buttons

        def exit_game():
            log.info("Exit pressed")
            # Start fade out before exiting
            self.start_fade_out()
            # We'll handle the actual exit after fade completes
            self._exit_requested = True

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

            # If all entities are fully transparent, handle the next action
            if all_faded:
                if hasattr(self, '_exit_requested') and self._exit_requested:
                    # Exit the application
                    self.app.running = False
                else:
                    # Start a new game
                    from .game import GameScene
                    self.app.scene_manager.change(GameScene(self.app))

    def start_fade_out(self):
        """Start the fade out animation before transitioning to the next scene"""
        self._fading_out = True
        for entity in self.entities:
            alpha_comp = entity.get(AlphaComponent)
            if alpha_comp:
                alpha_comp.target_alpha = 0.0  # Fade to transparent
