import logging

import pygame

from config import GameConfig
from engine import (
    BaseScene,
    ButtonComponent,
    InputFieldComponent,
    LabelComponent,
    ServiceLocator,
    UIBuilder,
)
from game.logic import GameLogic, GuessStatus

log = logging.getLogger("game/scenes")


class GameScene(BaseScene):
    def enter(self):
        log.info("GameScene enter")
        ui = UIBuilder(self.app.font)
        self.game_logic: GameLogic = ServiceLocator.get("game_logic")  # type: ignore

        # Check if we're returning from dialog cancel (preserve all game state)
        is_returning_from_dialog = (
            hasattr(self, "_from_dialog_cancel") and self._from_dialog_cancel
        )
        if is_returning_from_dialog:
            # Clear the flag and preserve game state
            self._from_dialog_cancel = False
            # Preserve existing values for history and other state
            preserved_history_list = getattr(self, "history_list", [])
            preserved_input_value = ""
            if hasattr(self, "input_ent"):
                input_comp = self.input_ent.get(InputFieldComponent)
                if input_comp:
                    preserved_input_value = input_comp.text
        else:
            # This is a new game session, reset everything
            self.game_logic.reset()
            # Note: GameLogic.reset() likely already generates a new number
            preserved_history_list = []
            preserved_input_value = ""

        title_text = f"Guess the number game {self.game_logic.min_number}-{self.game_logic.max_number}"
        self.title = ui.h1_entity(title_text, 320, 50)
        self.instructions = ui.h2_entity(
            "Enter the number and press Submit or Enter",
            320,
            100,
            GameConfig.HINT_COLOR,
        )
        # Error message positioned between instructions and input field
        self.error_label = ui.label_entity("", 320, 150, GameConfig.ERROR_COLOR)
        # Calculate max input length based on the max possible number
        max_input_len = len(str(self.game_logic.max_number))
        self.input_ent = ui.input_entity(
            "Enter the number", 320, 200, max_len=max_input_len
        )

        # Restore input value if returning from dialog
        if preserved_input_value:
            input_comp = self.input_ent.get(InputFieldComponent)
            if input_comp:
                input_comp.text = preserved_input_value

        self.history_label = ui.label_entity("", 320, 260, GameConfig.HINT_COLOR)
        self.attempts_label = ui.label_entity(
            f"Attempts: {self.game_logic.attempts}", 320, 300, GameConfig.HINT_COLOR
        )

        self._restart_requested = False

        def restart_click():
            log.info("Restart clicked")
            # Start fade out with a callback to reset and recreate the scene
            def on_fade_complete():
                # Change to a new GameScene which will start fresh
                self.app.scene_manager.change(GameScene(self.app))

            self.start_fade_out(on_complete_callback=on_fade_complete)

        # Create full-width buttons that span more of the container
        btn_width = 280
        btn_y = 360

        # Restart button - reposition to better distribute space
        self.btn_restart = ui.button_entity_with_min_width(
            "Reset", 160, btn_y, restart_click, btn_width
        )

        def submit_click():
            self.submit_guess()

        # Submit/Confirm button - reposition accordingly
        self.btn_submit = ui.button_entity_with_min_width(
            "Submit", 480, btn_y, submit_click, btn_width
        )

        # Initially set the submit button as inactive
        submit_component = self.btn_submit.get(ButtonComponent)
        if submit_component:
            submit_component.active = False

        # Back to menu - move to top right with appropriate padding
        def show_quit_confirmation():
            from .dialog import DialogScene

            def confirm_quit():
                # Start fade out with callback to go to menu
                from .menu import MenuScene
                def on_fade_complete():
                    self.app.scene_manager.change(MenuScene(self.app))

                self.app.scene_manager.current.start_fade_out(on_complete_callback=on_fade_complete)

            def cancel_quit():
                # Go back to the game scene without quitting, preserve game state
                self._from_dialog_cancel = True
                self.app.scene_manager.change(self)

            dialog_scene = DialogScene(
                self.app,
                "Confirm Exit",
                "Are you sure you want to go to Menu?",
                confirm_quit,
                cancel_quit,
                "Yes",
                "No",
            )
            self.app.scene_manager.change(dialog_scene)

        # Menu button at top right with appropriate padding
        menu_x = GameConfig.WINDOW_WIDTH - 50  # Positioned from right edge
        menu_y = 50  # Top padding to avoid being stuck to the top
        self.btn_menu = ui.button_entity("Menu", menu_x, menu_y, show_quit_confirmation)

        # Add alpha components to enable fade transitions
        from engine import AlphaComponent

        for entity in [
            self.title,
            self.instructions,
            self.input_ent,
            self.btn_submit,
            self.btn_restart,
            self.error_label,
            self.history_label,
            self.attempts_label,
            self.btn_menu,
        ]:
            entity.add(AlphaComponent(1.0))

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
        # Preserve history list if returning from dialog, otherwise start fresh
        if is_returning_from_dialog:
            self.history_list = preserved_history_list
        else:
            self.history_list: list[str] = []
        self.update_history_label()
        self.clear_error_label()  # Initially clear the error label

        # Input system focus the input on enter to scene
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
                error_msg = f"Number out of range: '{text}'"
                range_info = (
                    f"(use {self.game_logic.min_number}-{self.game_logic.max_number})"
                )
                self.show_error(f"{error_msg} {range_info}")
                return  # Don't clear input for out of range
            case GuessStatus.TOO_LOW:
                self.history_list.insert(0, f"{text} - Too Low")
            case GuessStatus.TOO_HIGH:
                self.history_list.insert(0, f"{text} - Too High")
            case GuessStatus.CORRECT:
                log.info("User guessed correctly")
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
            pygame.event.post(
                pygame.event.Event(pygame.USEREVENT, {"action": "clear_error"})
            )

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
            " | ".join(self.history_list[: GameConfig.SCENE_MAX_HISTORY_ENTRIES])
            if self.history_list
            else ""
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
                    # Start fade out with callback to go to menu
                    def on_fade_complete():
                        from .menu import MenuScene
                        self.app.scene_manager.change(MenuScene(self.app))

                    self.start_fade_out(on_complete_callback=on_fade_complete)
        # Handle custom event to clear error message
        elif (
            event.type == pygame.USEREVENT
            and hasattr(event, "action")
            and event.action == "clear_error"
        ):
            self.clear_error_label()

    def update_submit_button_state(self):
        """Update the submit button's active state and error message based on input validity"""
        input_field = self.input_ent.get(InputFieldComponent)
        submit_btn = self.btn_submit.get(ButtonComponent)
        error_label = self.error_label.get(LabelComponent)

        if input_field and submit_btn:
            text = input_field.text.strip()

            # Check for various validation errors
            if text == "":
                # No error when empty, just inactive button
                submit_btn.active = False
                if error_label:
                    error_label.text = ""
            elif not text.isdigit():
                # Not a number
                submit_btn.active = False
                if error_label:
                    error_label.text = "Invalid: Enter a number"
                    error_label.color = GameConfig.ERROR_COLOR
            else:
                # It's a number, check if it's in range using game logic's min/max
                num = int(text)
                if num < self.game_logic.min_number or num > self.game_logic.max_number:
                    submit_btn.active = False
                    if error_label:
                        invalid_msg = "Invalid: Number out of range"
                        range_vals = f"({self.game_logic.min_number}-{self.game_logic.max_number})"
                        error_label.text = f"{invalid_msg} {range_vals}"
                        error_label.color = GameConfig.ERROR_COLOR
                else:
                    # Valid input
                    submit_btn.active = True
                    if error_label:
                        error_label.text = ""

    def update(self, delta_time: float):
        # Update button states
        self.update_submit_button_state()

        # Call parent update to handle fade-out if in progress
        super().update(delta_time)  # This calls the BaseScene's update method which handles fade-out
