import logging
import pygame
import threading
import time
from engine import BaseScene, LabelComponent, InputFieldComponent
from game.ui_builder import UIBuilder
from game.logic import GameLogic, GuessStatus
from config import GameConfig
from engine import ServiceLocator


log = logging.getLogger("game/scenes")


class GameScene(BaseScene):
    def enter(self):
        log.info("GameScene enter")
        ui = UIBuilder(self.app.font)
        self.game_logic: GameLogic = ServiceLocator.get("game_logic")  # type: ignore

        # Use configuration values
        self.title = ui.label_entity("Guess the number game 1-100", 300, 50)
        self.instructions = ui.label_entity(
            "Enter the number and press Submit or Enter", 300, 100, GameConfig.HINT_COLOR
        )
        # Error message positioned between instructions and input field
        self.error_label = ui.label_entity("", 300, 130, GameConfig.ERROR_COLOR)
        self.input_ent = ui.input_entity("Enter the number", 300, 160, max_len=GameConfig.INPUT_MAX_LENGTH + 2)
        self.history_label = ui.label_entity("", 300, 210, GameConfig.HINT_COLOR)  # Only valid attempts (moved down)
        self.attempts_label = ui.label_entity(
            f"Attempts: {self.game_logic.attempts}", 300, 260, GameConfig.HINT_COLOR
        )

        def submit_click():
            self.submit_guess()

        # Center buttons at the bottom of the screen
        btn_spacing = 150  # Space between buttons
        center_x = 300
        btn_y = 350
        self.btn_submit = ui.button_entity("Submit", center_x - btn_spacing//2, btn_y, submit_click)

        # Restart button
        def restart_click():
            log.info("Restart clicked")
            self.game_logic.reset()
            input_field = self.input_ent.get(InputFieldComponent)
            if input_field is not None:
                input_field.clear()
            self.history_list = []
            self.clear_error_label()  # Clear error label on reset
            self.update_history_label()
            attempts_label_comp = self.attempts_label.get(LabelComponent)
            if attempts_label_comp is not None:
                attempts_label_comp.text = f"Attempts: {self.game_logic.attempts}"

        self.btn_restart = ui.button_entity("Reset", center_x + btn_spacing//2, btn_y, restart_click)

        # Back to menu - move to top right with appropriate padding
        def to_menu():
            # Import here to avoid circular imports
            from .menu import MenuScene
            self.app.scene_manager.change(MenuScene(self.app))

        # Menu button at top right with appropriate padding
        # Using a safe distance from the right edge to prevent going off screen
        menu_x = GameConfig.WINDOW_WIDTH - 50  # Positioned from right edge
        menu_y = 30  # More top padding to avoid being stuck to the top
        self.btn_menu = ui.button_entity("Menu", menu_x, menu_y, to_menu)

        self.entities = [
            self.title,
            self.instructions,
            self.input_ent,
            self.btn_submit,
            self.btn_restart,
            self.error_label,
            self.history_label,
            self.attempts_label,
            self.btn_menu,
        ]
        self.history_list: list[str] = []
        self.update_history_label()
        self.clear_error_label()  # Initially clear the error label

        # input system focus the input on enter to scene
        self.app.input_system.set_focus(self.input_ent.get(InputFieldComponent))

    def submit_guess(self):
        inp = self.input_ent.get(InputFieldComponent)
        if inp is None:
            log.error("InputFieldComponent not found in input_ent")
            return
        text = inp.text.strip()
        status = self.game_logic.check(text)

        match status:
            case GuessStatus.INVALID_FORMAT:
                self.show_error(f"Invalid input: '{text}'")
                return  # Don't clear input for invalid format
            case GuessStatus.OUT_OF_RANGE:
                self.show_error(f"Number out of range: '{text}' (use {self.game_logic.min_number}-{self.game_logic.max_number})")
                return  # Don't clear input for out of range
            case GuessStatus.TOO_LOW:
                self.history_list.insert(0, f"{text} - Too Low")
            case GuessStatus.TOO_HIGH:
                self.history_list.insert(0, f"{text} - Too High")
            case GuessStatus.CORRECT:
                log.info("User guessed correctly")
                # Import here to avoid circular imports
                from .win import WinScene
                self.app.scene_manager.change(
                    WinScene(self.app, self.game_logic.attempts)
                )
                return

        # For valid inputs, clear the input field and update attempts
        inp.clear()

        # Only update attempts if it was a valid numeric guess within range
        if status in [GuessStatus.TOO_LOW, GuessStatus.TOO_HIGH, GuessStatus.CORRECT]:
            attempts_label_comp = self.attempts_label.get(LabelComponent)
            if attempts_label_comp is not None:
                attempts_label_comp.text = f"Attempts: {self.game_logic.attempts}"

        self.update_history_label()

    def show_error(self, message: str):
        """Show an error message temporarily"""
        error_label_comp = self.error_label.get(LabelComponent)
        if error_label_comp is not None:
            error_label_comp.text = message
            error_label_comp.color = GameConfig.ERROR_COLOR

        # Clear the error message after 3 seconds
        import threading
        def clear_error_after_delay():
            import time
            time.sleep(3)
            # Use a callback to update UI from main thread to avoid threading issues
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {'action': 'clear_error'}))

        thread = threading.Thread(target=clear_error_after_delay)
        thread.daemon = True
        thread.start()

    def clear_error_label(self):
        """Clear the error message"""
        error_label_comp = self.error_label.get(LabelComponent)
        if error_label_comp is not None:
            error_label_comp.text = ""
            error_label_comp.color = GameConfig.TEXT_COLOR  # Reset to default color

    def update_history_label(self):
        # Use configuration value for max history entries
        compact = (
            " | ".join(self.history_list[:GameConfig.SCENE_MAX_HISTORY_ENTRIES]) if self.history_list else ""
        )
        label_comp = self.history_label.get(LabelComponent)
        if label_comp is not None:
            label_comp.text = compact

    def handle_event(self, event):
        # keyboard: Enter triggers submit, ESC -> menu
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_RETURN:
                    # when focused input exists submit
                    input_field = self.input_ent.get(InputFieldComponent)
                    if input_field is not None and input_field.text:
                        self.submit_guess()
                case pygame.K_ESCAPE:
                    # Import here to avoid circular imports
                    from .menu import MenuScene
                    self.app.scene_manager.change(MenuScene(self.app))
        # Handle custom event to clear error message
        elif event.type == pygame.USEREVENT and hasattr(event, 'action') and event.action == 'clear_error':
            self.clear_error_label()

    def update(self, dt: float):
        pass