import logging
import pygame
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
        self.history_label = ui.label_entity("", 300, 200, GameConfig.ERROR_COLOR)
        self.attempts_label = ui.label_entity(
            f"Attempts: {self.game_logic.attempts}", 300, 260, GameConfig.HINT_COLOR
        )

        self.input_ent = ui.input_entity("Enter the number", 300, 160, max_len=GameConfig.INPUT_MAX_LENGTH)

        def submit_click():
            self.submit_guess()

        self.btn_submit = ui.button_entity("Submit", 450, 160, submit_click)

        # Restart button
        def restart_click():
            log.info("Restart clicked")
            self.game_logic.reset()
            input_field = self.input_ent.get(InputFieldComponent)
            if input_field is not None:
                input_field.clear()
            self.history_list = []
            self.update_history_label()
            attempts_label_comp = self.attempts_label.get(LabelComponent)
            if attempts_label_comp is not None:
                attempts_label_comp.text = f"Attempts: {self.game_logic.attempts}"

        self.btn_restart = ui.button_entity("Reset", 150, 160, restart_click)

        # Back to menu
        def to_menu():
            # Import here to avoid circular imports
            from .menu import MenuScene
            self.app.scene_manager.change(MenuScene(self.app))

        self.btn_menu = ui.button_entity("Menu", 550, 350, to_menu)

        self.entities = [
            self.title,
            self.instructions,
            self.input_ent,
            self.btn_submit,
            self.btn_restart,
            self.history_label,
            self.attempts_label,
            self.btn_menu,
        ]
        self.history_list: list[str] = []
        self.update_history_label()

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
            case GuessStatus.INVALID:
                self.history_list.insert(0, f"Error: '{text}'")
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
        inp.clear()
        attempts_label_comp = self.attempts_label.get(LabelComponent)
        if attempts_label_comp is not None:
            attempts_label_comp.text = f"Attempts: {self.game_logic.attempts}"
        self.update_history_label()

    def update_history_label(self):
        # Use configuration value for max history entries
        compact = (
            " | ".join(self.history_list[:GameConfig.SCENE_MAX_HISTORY_ENTRIES]) if self.history_list else "Empty History"
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

    def update(self, dt: float):
        pass