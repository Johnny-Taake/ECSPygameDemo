from datetime import datetime
import sys

from config import GameConfig
from engine import AlphaComponent, BaseScene, ButtonComponent, UIBuilder
from logger import get_logger
from stats import get_difficulty_stats

log = get_logger("game/scenes")


def format_timestamp(ts: str) -> str:
    """Convert ISO timestamp into short readable format: 3 Dec'25"""
    dt = datetime.fromisoformat(ts)
    return (
        dt.strftime("%-d %b '%y")
        if sys.platform != "win32"
        else dt.strftime("%#d %b'%y")
    )


class WinScene(BaseScene):
    def __init__(self, app, attempts: int, game_logic=None):
        super().__init__(app)
        self.attempts = attempts
        self.game_logic = game_logic  # Store game logic to access difficulty info

    def enter(self):
        log.info("WinScene enter")
        ui = UIBuilder(self.app.font)

        self.title = ui.h1_entity("Correct!", 320, 100, GameConfig.SUCCESS_COLOR)
        self.stat = ui.h2_entity(
            f"Attempts: {self.attempts}", 320, 180, GameConfig.HINT_COLOR
        )

        # Get the timestamp of the most recent game with the same attempt count to identify the current game in the results modal
        self.current_game_timestamp = self._get_current_game_timestamp()

        # Check if this result is a new top score
        self.top_ranking = self._check_top_ranking()

        if self.top_ranking:
            if self.top_ranking == 1:
                rank_text = "NEW #1 SCORE!"
                rank_color = GameConfig.TOP_SCORE_1_COLOR
            elif self.top_ranking <= 3:
                rank_text = f"NEW TOP {self.top_ranking}!"
                rank_color = GameConfig.TOP_SCORE_2_TO_3_COLOR
            elif self.top_ranking <= 5:
                rank_text = f"NEW TOP {self.top_ranking}!"
                rank_color = GameConfig.TOP_SCORE_4_TO_5_COLOR
            else:
                rank_text = ""
                rank_color = GameConfig.TEXT_COLOR

            if rank_text:
                self.top_ranking_label = ui.h3_entity(rank_text, 320, 260, rank_color)
        else:
            # If not a top score, don't show the label
            rank_text = ""
            rank_color = GameConfig.TEXT_COLOR

        def to_menu():
            # Store the current difficulty in service locator before going to menu
            if self.game_logic is not None:
                from engine import ServiceLocator
                from config import GameConfig

                # Find the corresponding difficulty index to store
                config_difficulty_modes = GameConfig.DIFFICULTY_MODES
                matching_index = None
                for i, mode in enumerate(config_difficulty_modes):
                    if (
                        mode.min == self.game_logic.min_number
                        and mode.max == self.game_logic.max_number
                    ):
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
                    if (
                        mode.min == self.game_logic.min_number
                        and mode.max == self.game_logic.max_number
                    ):
                        matching_index = i
                        break

                if matching_index is not None:
                    ServiceLocator.provide("last_selected_difficulty", matching_index)

            from .game import GameScene

            # Start fade out with callback to go to game scene
            def on_fade_complete():
                self.app.scene_manager.change(GameScene(self.app))

            self.start_fade_out(on_complete_callback=on_fade_complete)

        def show_results():
            self.show_results()

        # Play win sound when the win scene is entered
        from engine import ServiceLocator

        sound_system = ServiceLocator.get("sound_system")
        if sound_system:
            sound_system.play_sound("win")

        def play_again_with_sound():
            # Play button click sound
            from engine import ServiceLocator

            sound_system = ServiceLocator.get("sound_system")
            if sound_system:
                sound_system.play_sound("button_click")
            start_play_again()

        def menu_with_sound():
            # Play button click sound
            from engine import ServiceLocator

            sound_system = ServiceLocator.get("sound_system")
            if sound_system:
                sound_system.play_sound("button_click")
            to_menu()

        def results_with_sound():
            # Play button click sound
            from engine import ServiceLocator

            sound_system = ServiceLocator.get("sound_system")
            if sound_system:
                sound_system.play_sound("button_click")
            show_results()

        # Create buttons with keyboard shortcut tags
        self.btn_play = ui.button_entity(
            "Play Again", 155, 340, play_again_with_sound, "[ENTER]"
        )
        # Set minimum width to match longest button text in scene
        play_component = self.btn_play.get(ButtonComponent)
        if play_component:
            play_component.min_width = 140

        self.btn_results = ui.button_entity(
            "View Results", 315, 340, results_with_sound, "[SPACE]"
        )
        # Set minimum width to match longest button text in scene
        results_component = self.btn_results.get(ButtonComponent)
        if results_component:
            results_component.min_width = 140

        self.btn_menu = ui.button_entity("Menu", 475, 340, menu_with_sound, "[ESC]")
        # Set minimum width to match longest button text in scene
        menu_component = self.btn_menu.get(ButtonComponent)
        if menu_component:
            menu_component.min_width = 140

        # Add alpha components to enable fade transitions
        entities_list = [
            self.title,
            self.stat,
            self.btn_play,
            self.btn_results,
            self.btn_menu,
        ]

        # Add top ranking label if it exists
        if hasattr(self, "top_ranking_label"):
            entities_list.append(self.top_ranking_label)

        for entity in entities_list:
            entity.add(AlphaComponent(1.0))

        self.entities = entities_list

    def _get_difficulty_name_from_range(self, min_num: int, max_num: int) -> str:
        """Get the name of the difficulty based on range."""
        for difficulty in GameConfig.DIFFICULTY_MODES:
            if difficulty.min == min_num and difficulty.max == max_num:
                return difficulty.name
        # If no predefined difficulty matches, create a custom name
        return f"Custom_{min_num}-{max_num}"

    def _check_top_ranking(self) -> int:
        """Check if the current result is a new top score and return the ranking, or 0 if not."""
        if not self.game_logic:
            return 0

        difficulty_name = self._get_difficulty_name_from_range(
            self.game_logic.min_number, self.game_logic.max_number
        )

        # Get the updated stats (the result was already recorded in game logic)
        difficulty_stats = get_difficulty_stats(
            difficulty_name, self.game_logic.min_number, self.game_logic.max_number
        )

        top_attempts = difficulty_stats["top_attempts"]

        # Find the rank of the specific current game by looking for the entry with the specific timestamp
        for i, attempt in enumerate(top_attempts):
            if (
                attempt["attempts"] == self.attempts
                and attempt["timestamp"] == self.current_game_timestamp
            ):
                rank = i + 1  # 1-indexed
                # Only return the ranking if it's in the top 5 (or if it made it into the top list)
                if rank <= GameConfig.STATS_MAX_TOP_ATTEMPTS:
                    return rank
                else:
                    return 0

        # If the current game result is not found in the top list, it's not a top score
        return 0

    def _get_current_game_timestamp(self) -> str:
        """Get the timestamp of the current game result from the stats."""
        if not self.game_logic:
            return ""

        difficulty_name = self._get_difficulty_name_from_range(
            self.game_logic.min_number, self.game_logic.max_number
        )

        # Get the updated stats (the result was already recorded in game logic)
        difficulty_stats = get_difficulty_stats(
            difficulty_name, self.game_logic.min_number, self.game_logic.max_number
        )

        top_attempts = difficulty_stats["top_attempts"]

        # Find the most recent timestamp for a game with the same number of attempts
        # This will be the current game since it was the most recently added
        current_game_timestamp = ""
        latest_timestamp = ""

        for attempt in top_attempts:
            if (
                attempt["attempts"] == self.attempts
                and attempt["timestamp"] > latest_timestamp
            ):
                latest_timestamp = attempt["timestamp"]
                current_game_timestamp = attempt["timestamp"]

        return current_game_timestamp

    def show_results(self):
        """Show the results modal"""
        if self.game_logic:
            difficulty_name = self._get_difficulty_name_from_range(
                self.game_logic.min_number, self.game_logic.max_number
            )

            from .results_modal import ResultsModalScene

            modal_scene = ResultsModalScene(
                self.app,
                difficulty_name,
                self.game_logic.min_number,
                self.game_logic.max_number,
                current_attempts=self.attempts,
                current_ranking=self.top_ranking,
                current_timestamp=self.current_game_timestamp,
            )
            # Store reference to current scene so modal can return to it
            modal_scene.previous_scene = self
            self.app.scene_manager.change(modal_scene)

    def handle_event(self, event):
        import pygame

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.start_play_again()
            elif event.key == pygame.K_ESCAPE:
                self.to_menu()
            elif event.key == pygame.K_SPACE:
                self.show_results()

    def to_menu(self):
        # Play button click sound
        from engine import ServiceLocator

        sound_system = ServiceLocator.get("sound_system")
        if sound_system:
            sound_system.play_sound("button_click")

        # Store the current difficulty in service locator before going to menu
        if self.game_logic is not None:
            from engine import ServiceLocator
            from config import GameConfig

            # Find the corresponding difficulty index to store
            config_difficulty_modes = GameConfig.DIFFICULTY_MODES
            matching_index = None
            for i, mode in enumerate(config_difficulty_modes):
                if (
                    mode.min == self.game_logic.min_number
                    and mode.max == self.game_logic.max_number
                ):
                    matching_index = i
                    break

            if matching_index is not None:
                ServiceLocator.provide("last_selected_difficulty", matching_index)

        # Start fade out with callback to go to menu
        def on_fade_complete():
            from .menu import MenuScene

            self.app.scene_manager.change(MenuScene(self.app))

        self.start_fade_out(on_complete_callback=on_fade_complete)

    def start_play_again(self):
        # Play button click sound
        from engine import ServiceLocator

        sound_system = ServiceLocator.get("sound_system")
        if sound_system:
            sound_system.play_sound("button_click")

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
                if (
                    mode.min == self.game_logic.min_number
                    and mode.max == self.game_logic.max_number
                ):
                    matching_index = i
                    break

            if matching_index is not None:
                ServiceLocator.provide("last_selected_difficulty", matching_index)

        from .game import GameScene

        # Start fade out with callback to go to game scene
        def on_fade_complete():
            self.app.scene_manager.change(GameScene(self.app))

        self.start_fade_out(on_complete_callback=on_fade_complete)
