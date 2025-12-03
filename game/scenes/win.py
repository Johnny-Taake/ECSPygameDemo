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

        self.title = ui.h1_entity("Correct!", 300, 100, GameConfig.SUCCESS_COLOR)
        self.stat = ui.h2_entity(
            f"Attempts: {self.attempts}", 300, 160, GameConfig.HINT_COLOR
        )

        # Display game statistics if game_logic is available
        if self.game_logic:
            # Find the difficulty name based on range
            difficulty_name = self._get_difficulty_name_from_range(
                self.game_logic.min_number, self.game_logic.max_number
            )

            # Get stats for current difficulty
            difficulty_stats = get_difficulty_stats(
                difficulty_name, self.game_logic.min_number, self.game_logic.max_number
            )

            # Create statistics display - positioned in the top-right corner
            games_played = difficulty_stats["games_played"]
            top_attempts = difficulty_stats["top_attempts"]

            # stats_x = GameConfig.WINDOW_WIDTH - 100  # 100px from the right edge
            stats_x = 210
            # stats_start_y = 120
            stats_start_y = 210

            # Add games played label in the top-right
            self.games_played_label = ui.label_entity(
                f"Games played: {games_played}",
                stats_x,
                stats_start_y,
                GameConfig.HINT_COLOR,
            )

            # Add top scores header in the top-right
            self.top_scores_header = ui.h3_entity(
                "Top Scores:", stats_x, stats_start_y + 30, GameConfig.TEXT_COLOR
            )

            # Add top 10 attempts (or fewer if available) in the top-right
            if top_attempts:
                start_y = stats_start_y + 60  # Start below the header
                for i, attempt in enumerate(
                    top_attempts[:5]
                ):  # Show top 5 to avoid crowding
                    y_pos = start_y + (i * 20)  # 20px spacing between entries
                    attempt_text = f"#{i+1}: {attempt['attempts']} att. - {format_timestamp(attempt['timestamp'])}"
                    label = ui.label_entity(
                        attempt_text, stats_x, y_pos, GameConfig.TEXT_COLOR
                    )
                    setattr(
                        self, f"top_score_label_{i}", label
                    )  # Store as instance attribute
            else:
                no_scores = ui.label_entity(
                    "No scores yet", stats_x, stats_start_y + 60, GameConfig.HINT_COLOR
                )
                self.no_scores_label = no_scores

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

        # Create buttons with keyboard shortcut tags
        self.btn_play = ui.button_entity(
            "Play Again", 470, 270, play_again_with_sound, "[ENTER]"
        )
        # Set minimum width to match longest button text in scene
        play_component = self.btn_play.get(ButtonComponent)
        if play_component:
            play_component.min_width = 140

        self.btn_menu = ui.button_entity("Menu", 470, 330, menu_with_sound, "[ESC]")
        # Set minimum width to match longest button text in scene
        menu_component = self.btn_menu.get(ButtonComponent)
        if menu_component:
            menu_component.min_width = 140

        # Add alpha components to enable fade transitions
        entities_list = [self.title, self.stat, self.btn_play, self.btn_menu]

        # Add stat display entities if they were created
        if hasattr(self, "games_played_label"):
            entities_list.append(self.games_played_label)
        if hasattr(self, "top_scores_header"):
            entities_list.append(self.top_scores_header)
        if hasattr(self, "no_scores_label"):
            entities_list.append(self.no_scores_label)

        # Add top score labels if they exist
        for i in range(5):
            label_attr = f"top_score_label_{i}"
            if hasattr(self, label_attr):
                entities_list.append(getattr(self, label_attr))

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

    def handle_event(self, event):
        import pygame

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.start_play_again()
            elif event.key == pygame.K_ESCAPE:
                self.to_menu()

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

    def update(self, delta_time: float):
        # Call parent update to handle fade-out if in progress
        super().update(
            delta_time
        )  # This calls the BaseScene's update method which handles fade-out
