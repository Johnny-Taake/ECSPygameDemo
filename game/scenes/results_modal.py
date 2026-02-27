"""Modal scene for displaying game results and statistics."""

from typing import Optional

from config import GameConfig
from engine import AlphaComponent, BaseScene, ButtonComponent, UIBuilder
from logger import get_logger
from stats import get_difficulty_stats
from utils import format_timestamp

log = get_logger("game/scenes")


class ResultsModalScene(BaseScene):
    def __init__(
        self,
        app,
        difficulty_name: str,
        min_number: int,
        max_number: int,
        current_attempts: Optional[int] = None,
        current_ranking: int = 0,
        current_timestamp: str = "",
        previous_scene: Optional[BaseScene] = None,
    ):
        super().__init__(app)
        self.difficulty_name = difficulty_name
        self.min_number = min_number
        self.max_number = max_number
        self.current_attempts = current_attempts  # The attempts from the current game
        self.current_ranking = current_ranking  # The ranking of the current game
        self.current_timestamp = current_timestamp  # The timestamp of the current game
        self.previous_scene = previous_scene

    def enter(self):
        log.info(
            f"ResultsModalScene enter - {self.difficulty_name} ({self.min_number}-{
                self.max_number})"
        )
        ui = UIBuilder(self.app.font)

        # Create a semi-transparent background overlay
        overlay_entity = ui.label_entity("", 320, 240)
        overlay_entity.add(AlphaComponent(0.6))

        # Modal title
        self.title = ui.h2_entity(
            f"{self.difficulty_name} Stats", 320, 100, GameConfig.TEXT_COLOR
        )

        # Get stats for current difficulty
        difficulty_stats = get_difficulty_stats(
            self.difficulty_name, self.min_number, self.max_number
        )

        # Display games played
        self.games_played_label = ui.label_entity(
            f"Games played: {difficulty_stats['games_played']}",
            320,
            140,
            GameConfig.HINT_COLOR,
        )

        # Top scores header
        self.top_scores_header = ui.h3_entity(
            "Top Scores:", 320, 180, GameConfig.TEXT_COLOR
        )

        # Display top attempts (or fewer if available)
        top_attempts = difficulty_stats["top_attempts"]

        if top_attempts:
            start_y = 220
            # Show top stats up to the configured max to avoid crowding the UI
            max_display_attempts = min(
                len(top_attempts), GameConfig.SCENE_MAX_WIN_TOP_SCORES
            )
            for i, attempt in enumerate(top_attempts[:max_display_attempts]):
                y_pos = start_y + (i * 25)  # 25px spacing between entries
                attempt_text = f"#{
                    i+1}: {attempt['attempts']} att. - {format_timestamp(attempt['timestamp'])}"

                # Determine color based on whether this is the current attempt with the exact timestamp
                attempt_color = GameConfig.TEXT_COLOR
                # Highlight if this attempt matches the current game's attempt count AND timestamp
                if (
                    self.current_attempts is not None
                    and attempt["attempts"] == self.current_attempts
                    and attempt["timestamp"] == self.current_timestamp
                ):
                    # This is the current attempt, so use the appropriate highlight color based on ranking
                    if self.current_ranking == 1:
                        attempt_color = GameConfig.TOP_SCORE_1_COLOR
                    elif self.current_ranking <= 3:
                        attempt_color = GameConfig.TOP_SCORE_2_TO_3_COLOR
                    elif self.current_ranking <= 5:
                        attempt_color = GameConfig.TOP_SCORE_4_TO_5_COLOR

                label = ui.label_entity(
                    attempt_text, 320, y_pos, attempt_color)
                setattr(
                    self, f"top_score_label_{i}", label
                )  # Store as instance attribute
        else:
            no_scores = ui.label_entity(
                "No scores yet", 320, 220, GameConfig.HINT_COLOR
            )
            self.no_scores_label = no_scores

        def close_modal():
            self.close_modal()

        # Close button (positioned in the top-right corner of the modal)
        self.btn_close = ui.button_entity(
            "Close", 550, 100, close_modal, "[ESC]")

        # Set minimum width to match
        close_component = self.btn_close.get(ButtonComponent)
        if close_component:
            close_component.min_width = 100

        # Add alpha components to enable fade transitions
        entities_list = [
            overlay_entity,
            self.title,
            self.games_played_label,
            self.top_scores_header,
            self.btn_close,
        ]

        # Add stat display entities if they were created
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

    def handle_event(self, event):
        import pygame

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close_modal()

    def close_modal(self):
        log.info("Closing results modal")
        # Play button click sound
        from engine import ServiceLocator

        sound_system = ServiceLocator.get("sound_system")
        if sound_system:
            sound_system.play_sound("button_click")

        # Go back to the previous scene (typically the win scene)
        if hasattr(self, "previous_scene") and self.previous_scene:
            self.app.scene_manager.change(self.previous_scene)
        else:
            # Fallback to going back to menu
            from .menu import MenuScene

            self.app.scene_manager.change(MenuScene(self.app))

    def update(self, delta_time: float):
        # Call parent update to handle fade-out if in progress
        super().update(delta_time)
