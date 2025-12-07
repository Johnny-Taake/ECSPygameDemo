"""Main game configuration using Pydantic and pydantic-settings."""

from pydantic import BaseModel

from .base import ColorConfig, WindowConfig, DifficultyConfig
from .logging import LoggingConfig
from .stats import StatsConfig
from .ui import UIConfig


class GameConfig(BaseModel):
    """Main configuration class containing all game settings."""

    window: WindowConfig = WindowConfig()
    difficulty: DifficultyConfig = DifficultyConfig()
    colors: ColorConfig = ColorConfig()
    stats: StatsConfig = StatsConfig()
    ui: UIConfig = UIConfig()
    logging: LoggingConfig = LoggingConfig()

    @property
    def WINDOW_WIDTH(self) -> int:
        return self.window.width

    @property
    def WINDOW_HEIGHT(self) -> int:
        return self.window.height

    @property
    def FPS(self) -> int:
        return self.window.fps

    @property
    def WINDOW_TITLE(self) -> str:
        return self.window.title

    @property
    def BACKGROUND_COLOR(self) -> tuple:
        return self.colors.background_color

    @property
    def TEXT_COLOR(self) -> tuple:
        return self.colors.text_color

    @property
    def HINT_COLOR(self) -> tuple:
        return self.colors.hint_color

    @property
    def SHORTCUT_TAG_COLOR(self) -> tuple:
        return self.colors.shortcut_tag_color

    @property
    def SUCCESS_COLOR(self) -> tuple:
        return self.colors.success_color

    @property
    def ERROR_COLOR(self) -> tuple:
        return self.colors.error_color

    @property
    def BUTTON_BG_COLOR(self) -> tuple:
        return self.colors.button_bg_color

    @property
    def BUTTON_HOVER_COLOR(self) -> tuple:
        return self.colors.button_hover_color

    @property
    def DEFAULT_FONT(self) -> str:
        return self.ui.default_font

    @property
    def DEFAULT_FONT_PATH(self) -> str:
        return self.ui.default_font_path

    @property
    def ITALIC_FONT_PATH(self) -> str:
        return self.ui.italic_font_path

    @property
    def BOLD_FONT_PATH(self) -> str:
        return self.ui.bold_font_path

    @property
    def DEFAULT_FONT_SIZE(self) -> int:
        return self.ui.default_font_size

    @property
    def BUTTON_PADDING(self) -> int:
        return self.ui.button_padding

    @property
    def BUTTON_RADIUS(self) -> int:
        return self.ui.button_radius

    @property
    def LOG_LEVEL(self):
        return self.logging.log_level_enum

    @property
    def LOG_FORMAT(self) -> str:
        return self.logging.log_format

    @property
    def SCENE_TITLE_POSITION(self) -> tuple:
        return self.ui.scene_title_position

    @property
    def SCENE_SUBTITLE_POSITION(self) -> tuple:
        return self.ui.scene_subtitle_position

    @property
    def SCENE_BUTTON_START_POSITION(self) -> tuple:
        return self.ui.scene_button_start_position

    @property
    def SCENE_BUTTON_EXIT_POSITION(self) -> tuple:
        return self.ui.scene_button_exit_position

    @property
    def SCENE_MAX_HISTORY_ENTRIES(self) -> int:
        return self.ui.scene_max_history_entries

    @property
    def SCENE_MAX_WIN_TOP_SCORES(self) -> int:
        return self.ui.scene_max_win_top_scores

    @property
    def DIFFICULTY_MODES(self):
        """Get the list of difficulty modes."""
        return self.difficulty.modes

    @property
    def DEFAULT_DIFFICULTY_INDEX(self):
        """Get the default difficulty index."""
        return self.difficulty.default_index

    # Component defaults
    @property
    def LABEL_DEFAULT_COLOR(self) -> tuple:
        return self.colors.label_default_color

    @property
    def H1_DEFAULT_COLOR(self) -> tuple:
        return self.colors.h1_default_color

    @property
    def H2_DEFAULT_COLOR(self) -> tuple:
        return self.colors.h2_default_color

    @property
    def H3_DEFAULT_COLOR(self) -> tuple:
        return self.colors.h3_default_color

    @property
    def PROGRESS_BAR_BG_COLOR(self) -> tuple:
        return self.colors.progress_bar_bg_color

    @property
    def PROGRESS_BAR_FILL_COLOR(self) -> tuple:
        return self.colors.progress_bar_fill_color

    @property
    def INPUT_UNDERLINE_COLOR(self) -> tuple:
        return self.colors.input_underline_color

    @property
    def INACTIVE_BUTTON_GRAYED_COLOR(self) -> tuple:
        return self.colors.inactive_button_grayed_color

    @property
    def INACTIVE_BUTTON_BG_COLOR(self) -> tuple:
        return self.colors.inactive_button_bg_color

    @property
    def ACTIVE_BUTTON_TEXT_COLOR(self) -> tuple:
        return self.colors.active_button_text_color

    @property
    def PROGRESS_BAR_BORDER_COLOR(self) -> tuple:
        return self.colors.progress_bar_border_color

    @property
    def TOP_SCORE_1_COLOR(self) -> tuple:
        return self.colors.top_score_1_color

    @property
    def TOP_SCORE_2_TO_3_COLOR(self) -> tuple:
        return self.colors.top_score_2_to_3_color

    @property
    def TOP_SCORE_4_TO_5_COLOR(self) -> tuple:
        return self.colors.top_score_4_to_5_color

    # Font sizes
    @property
    def H1_FONT_SIZE(self) -> int:
        return self.ui.h1_font_size

    @property
    def H2_FONT_SIZE(self) -> int:
        return self.ui.h2_font_size

    @property
    def H3_FONT_SIZE(self) -> int:
        return self.ui.h3_font_size

    @property
    def BUTTON_TAG_FONT_SIZE(self) -> int:
        return self.ui.button_tag_font_size

    # Component defaults
    @property
    def INPUT_FIELD_DEFAULT_MAX_LENGTH(self) -> int:
        return self.ui.input_field_default_max_length

    @property
    def PROGRESS_BAR_ANIMATION_SPEED(self) -> float:
        return self.ui.progress_bar_animation_speed

    @property
    def ALPHA_ANIMATION_SPEED(self) -> float:
        return self.ui.alpha_animation_speed

    @property
    def PROGRESS_BAR_BORDER_RADIUS(self) -> int:
        return self.ui.progress_bar_border_radius

    @property
    def INPUT_FIELD_WIDTH(self) -> int:
        return self.ui.input_field_width

    @property
    def INPUT_FIELD_FONT_SIZE(self) -> int:
        return self.ui.input_field_font_size

    @property
    def INPUT_MOUSE_DETECTION_WIDTH(self) -> int:
        return self.ui.input_mouse_detection_width

    @property
    def INPUT_MOUSE_DETECTION_HEIGHT(self) -> int:
        return self.ui.input_mouse_detection_height

    @property
    def TEXT_MAX_WIDTH(self) -> int:
        # Calculate max text width as a percentage of screen width to maintain proper proportions
        # Use 90% of screen width as default maximum text width
        return int(self.window.width * 0.90)

    # Stats configuration
    @property
    def STATS_ENCRYPTION_KEY(self) -> str:
        return self.stats.encryption_key

    @property
    def STATS_FILE_NAME(self) -> str:
        return self.stats.stats_file_name

    @property
    def STATS_APP_DATA_DIR_NAME(self) -> str:
        return self.stats.app_data_dir_name

    @property
    def STATS_MAX_TOP_ATTEMPTS(self) -> int:
        return self.stats.max_top_attempts
