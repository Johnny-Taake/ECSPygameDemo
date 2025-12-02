import logging
import pygame

from engine import EventBus, ServiceLocator, LabelComponent, InputFieldComponent, BaseScene

from .logic import GameLogic, GuessStatus
from .ui_builder import UIBuilder


log = logging.getLogger("game/scenes")


class BootScene(BaseScene):
    def enter(self):
        event_bus = EventBus()
        ServiceLocator.provide("event_bus", event_bus)
        ServiceLocator.provide("game_logic", GameLogic(1, 100))

        log.info("BootScene enter")

        self.app.scene_manager.change(MenuScene(self.app))


class MenuScene(BaseScene):
    def enter(self):
        log.info("MenuScene enter")
        ui = UIBuilder(self.app.font)
        self.title = ui.label_entity("Guess The Number", 300, 80)
        self.subtitle = ui.label_entity("Press Start", 300, 130, (200, 200, 200))

        def start_game():
            log.info("Start pressed")
            self.app.scene_manager.change(GameScene(self.app))

        self.btn_start = ui.button_entity("Start", 300, 240, start_game)

        def exit_game():
            log.info("Exit pressed")
            self.app.running = False

        self.btn_exit = ui.button_entity("EXIT", 300, 300, exit_game)

        self.entities = [self.title, self.subtitle, self.btn_start, self.btn_exit]

    def handle_event(self, event):
        # mouse clicks routed by InputSystem
        pass


class WinScene(BaseScene):
    def __init__(self, app, attempts: int):
        super().__init__(app)
        self.attempts = attempts

    def enter(self):
        log.info("WinScene enter")
        ui = UIBuilder(self.app.font)

        self.title = ui.label_entity("Correct!", 300, 100, (150, 255, 150))
        self.stat = ui.label_entity(
            f"Attempts: {self.attempts}", 300, 160, (230, 230, 230)
        )

        def play_again():
            log.info("Play again")
            self.app.scene_manager.change(GameScene(self.app))

        def menu():
            log.info("To menu")
            self.app.scene_manager.change(MenuScene(self.app))

        self.btn_play = ui.button_entity("Play Again", 300, 250, play_again)
        self.btn_menu = ui.button_entity("Menu", 300, 310, menu)

        self.entities = [self.title, self.stat, self.btn_play, self.btn_menu]


class GameScene(BaseScene):
    def enter(self):
        log.info("GameScene enter")
        ui = UIBuilder(self.app.font)
        self.game_logic: GameLogic = ServiceLocator.get("game_logic")  # type: ignore

        # TODO: Move out variables
        self.title = ui.label_entity("Guess the number game 1-100", 300, 50)
        self.instructions = ui.label_entity(
            "Enter the number and press Submit or Enter", 300, 100, (200, 200, 200)
        )
        self.history_label = ui.label_entity("", 300, 200, (200, 180, 180))
        self.attempts_label = ui.label_entity(
            f"Attempts: {self.game_logic.attempts}", 300, 260, (200, 200, 200)
        )

        self.input_ent = ui.input_entity("Enter the number", 300, 160, max_len=3)

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
        # show up to 6 last entries
        compact = (
            " | ".join(self.history_list[:6]) if self.history_list else "Empty History"
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
                    self.app.scene_manager.change(MenuScene(self.app))

    def update(self, dt: float):
        pass
