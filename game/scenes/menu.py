from config import GameConfig
from engine import (
    AlphaComponent,
    BaseScene,
    ButtonComponent,
    InputFieldComponent,
    LabelComponent,
    ServiceLocator,
    UIBuilder,
)
from engine.event_bus import EventBus
from logger import get_logger

log = get_logger("game/scenes")


class MenuScene(BaseScene):
    def enter(self):
        log.info("MenuScene enter")
        self._exit_requested = False
        self._fading_out = False

        # Get difficulty settings from configuration
        config_difficulty_modes = GameConfig.DIFFICULTY_MODES
        # Convert to the internal format expected by the code
        self.difficulty_modes = [
            {"name": mode.name, "min": mode.min, "max": mode.max}
            for mode in config_difficulty_modes
        ]

        # Initialize to the configured default difficulty index
        self.current_difficulty_index = GameConfig.DEFAULT_DIFFICULTY_INDEX

        ui = UIBuilder(self.app.font)
        self.title = ui.h1_entity("Guess The Number", 300, 60)
        self.subtitle = ui.h2_entity("Press START", 300, 105, GameConfig.HINT_COLOR)

        # Difficulty selection UI
        self.difficulty_label = ui.label_entity(
            "Difficulty:", 300, 150, GameConfig.TEXT_COLOR
        )

        # Display current difficulty
        self.current_difficulty_text = ui.label_entity(
            self.get_current_difficulty_text(), 300, 175, GameConfig.TEXT_COLOR
        )

        # Left arrow for previous difficulty
        def prev_difficulty():
            self.current_difficulty_index = (self.current_difficulty_index - 1) % len(
                self.difficulty_modes
            )
            self.update_difficulty_display()

        self.btn_prev = ui.button_entity("<", 240, 220, prev_difficulty)
        prev_component = self.btn_prev.get(ButtonComponent)
        if prev_component:
            prev_component.min_width = 100

        # Right arrow for next difficulty
        def next_difficulty():
            self.current_difficulty_index = (self.current_difficulty_index + 1) % len(
                self.difficulty_modes
            )
            self.update_difficulty_display()

        self.btn_next = ui.button_entity(">", 360, 220, next_difficulty)
        next_component = self.btn_next.get(ButtonComponent)
        if next_component:
            next_component.min_width = 100

        def start_game():
            log.info("Start pressed")

            # Emit difficulty event via EventBus
            event_bus = ServiceLocator.get("event_bus")
            if not isinstance(event_bus, EventBus):
                log.error("event_bus not found in ServiceLocator")
                return
            current_difficulty = self.difficulty_modes[self.current_difficulty_index]
            event_bus.emit(
                "difficulty_selected",
                {
                    "min_number": current_difficulty["min"],
                    "max_number": current_difficulty["max"],
                    "name": current_difficulty["name"],
                },
            )

            # Update game logic in service locator with the selected difficulty as backup
            from game.logic import GameLogic

            new_game_logic = GameLogic(
                min_number=current_difficulty["min"],
                max_number=current_difficulty["max"],
            )
            ServiceLocator.provide("game_logic", new_game_logic)

            # Start fade out with callback to start the game
            def on_fade_complete():
                from .game import GameScene

                self.app.scene_manager.change(GameScene(self.app))

            self.start_fade_out(on_complete_callback=on_fade_complete)

        self.btn_start = ui.button_entity(
            "START", 300, 280, start_game
        )  # Center adjusted to match other UI elements, Y position updated for proper spacing
        # Set minimum width to match the width of difficulty buttons row
        start_component = self.btn_start.get(ButtonComponent)
        if start_component:
            start_component.min_width = (
                220  # Same total width as difficulty buttons (100 + 20 gap + 100)
            )

        def exit_game():
            log.info("Exit pressed")

            # Start fade out with callback to exit the application
            def on_fade_complete():
                self.app.running = False

            self.start_fade_out(on_complete_callback=on_fade_complete)

        self.btn_exit = ui.button_entity(
            "EXIT", 300, 340, exit_game
        )  # Center adjusted to match other UI elements, Y position updated for proper spacing
        # Set minimum width to match the width of difficulty buttons row
        exit_component = self.btn_exit.get(ButtonComponent)
        if exit_component:
            exit_component.min_width = (
                220  # Same total width as difficulty buttons (100 + 20 gap + 100)
            )

        # Add alpha components to enable fade transitions
        all_entities = [
            self.title,
            self.subtitle,
            self.difficulty_label,
            self.btn_prev,
            self.current_difficulty_text,
            self.btn_next,
            self.btn_start,
            self.btn_exit,
        ]

        for entity in all_entities:
            entity.add(AlphaComponent(1.0))

        self.entities = all_entities

    def get_current_difficulty_text(self):
        """Get text for current difficulty"""
        current = self.difficulty_modes[self.current_difficulty_index]
        return f"{current['name']}: {current['min']}-{current['max']}"

    def update_difficulty_display(self):
        """Update the difficulty display text"""
        # Update difficulty text
        difficulty_text_comp = self.current_difficulty_text.get(LabelComponent)
        if difficulty_text_comp:
            difficulty_text_comp.text = self.get_current_difficulty_text()

    def handle_event(self, event):
        # mouse clicks routed by InputSystem
        pass

    def update(self, delta_time: float):
        # Call parent update to handle fade-out if in progress
        super().update(
            delta_time
        )  # This calls the BaseScene's update method which handles fade-out
