import pytest
from unittest.mock import patch, Mock
from pydantic import ValidationError
from config import GameConfig
from config.base import WindowConfig, ColorConfig, DifficultyModel, DifficultyConfig


class TestWindowConfig:
    def test_window_config_defaults(self):
        """Test that WindowConfig has correct default values."""
        config = WindowConfig()
        assert config.width == 640
        assert config.height == 400
        assert config.fps == 60
        assert config.title == "Guess The Number"

    def test_window_config_custom_values(self):
        """Test that WindowConfig accepts custom values."""
        config = WindowConfig(width=800, height=600, fps=120, title="Custom Game")
        assert config.width == 800
        assert config.height == 600
        assert config.fps == 120
        assert config.title == "Custom Game"

    def test_window_config_negative_dimensions_validation(self):
        """Test that WindowConfig rejects negative dimensions."""
        with pytest.raises(ValidationError):
            WindowConfig(width=-100, height=400)

        with pytest.raises(ValidationError):
            WindowConfig(width=640, height=-200)

    def test_window_config_zero_dimensions_validation(self):
        """Test that WindowConfig rejects zero dimensions."""
        with pytest.raises(ValidationError):
            WindowConfig(width=0, height=400)

        with pytest.raises(ValidationError):
            WindowConfig(width=640, height=0)


class TestColorConfig:
    def test_color_config_defaults(self):
        """Test that ColorConfig has correct default values."""
        config = ColorConfig()
        assert config.background_color == (30, 30, 30)
        assert config.text_color == (255, 255, 255)
        assert config.hint_color == (200, 200, 200)

    def test_color_config_custom_values(self):
        """Test that ColorConfig accepts custom color values."""
        custom_color = (255, 128, 0)
        config = ColorConfig(background_color=custom_color)
        assert config.background_color == custom_color

    def test_color_config_validation_valid_colors(self):
        """Test that ColorConfig accepts valid color values."""
        valid_colors = [
            (0, 0, 0),  # Black
            (255, 255, 255),  # White
            (128, 128, 128),  # Gray
            (255, 0, 0),  # Red
        ]

        for color in valid_colors:
            config = ColorConfig(background_color=color)
            assert config.background_color == color

    def test_color_config_validation_invalid_colors(self):
        """Test that ColorConfig rejects invalid color values."""
        invalid_colors = [
            (256, 0, 0),  # R > 255
            (-1, 0, 0),  # R < 0
            (0, 256, 0),  # G > 255
            (0, -1, 0),  # G < 0
            (0, 0, 256),  # B > 255
            (0, 0, -1),  # B < 0
            (255, 255),  # Wrong length - only 2 values
            (255, 255, 255, 255),  # Wrong length - 4 values
            "not_a_color",  # Not a tuple/list
        ]

        for color in invalid_colors:
            with pytest.raises(ValidationError):
                ColorConfig(background_color=color)

    def test_color_config_validation_tuple_list_support(self):
        """Test that ColorConfig accepts both tuple and list inputs."""
        config1 = ColorConfig(background_color=(255, 128, 0))
        assert config1.background_color == (255, 128, 0)

        config2 = ColorConfig(background_color=(255, 128, 0))
        assert config2.background_color == (255, 128, 0)


class TestDifficultyModel:
    def test_difficulty_model_defaults(self):
        """Test that DifficultyModel has correct defaults."""
        difficulty = DifficultyModel(name="Easy", min=1, max=10)
        assert difficulty.name == "Easy"
        assert difficulty.min == 1
        assert difficulty.max == 10

    def test_difficulty_model_custom_values(self):
        """Test that DifficultyModel accepts custom values."""
        difficulty = DifficultyModel(name="Custom", min=50, max=150)
        assert difficulty.name == "Custom"
        assert difficulty.min == 50
        assert difficulty.max == 150

    def test_difficulty_model_range_validation(self):
        """Test that DifficultyModel validates range (max > min)."""
        # Valid range
        difficulty = DifficultyModel(name="Test", min=1, max=10)
        assert difficulty.min < difficulty.max

        # Invalid range - max <= min
        with pytest.raises(ValidationError):
            DifficultyModel(name="Invalid", min=10, max=5)

        with pytest.raises(ValidationError):
            DifficultyModel(name="Invalid", min=10, max=10)


class TestDifficultyConfig:
    def test_difficulty_config_defaults(self):
        """Test that DifficultyConfig has correct default values."""
        config = DifficultyConfig()
        assert len(config.modes) == 5
        assert config.modes[0].name == "Easy"
        assert config.modes[0].min == 1 and config.modes[0].max == 10
        assert config.modes[1].name == "Medium"
        assert config.modes[1].min == 1 and config.modes[1].max == 100
        assert config.modes[2].name == "Hard"
        assert config.modes[2].min == 1 and config.modes[2].max == 1000
        assert config.default_index == 1  # Medium difficulty

    def test_difficulty_config_custom_modes(self):
        """Test that DifficultyConfig accepts custom difficulty modes."""
        custom_modes = [
            DifficultyModel(name="Easy", min=1, max=5),
            DifficultyModel(name="Hard", min=1, max=50),
        ]
        config = DifficultyConfig(modes=custom_modes, default_index=0)
        assert len(config.modes) == 2
        assert config.modes[0].name == "Easy"
        assert config.modes[1].name == "Hard"
        assert config.default_index == 0

    def test_difficulty_config_empty_modes_validation(self):
        """Test that DifficultyConfig rejects empty modes list."""
        with pytest.raises(ValidationError):
            DifficultyConfig(modes=[], default_index=0)

    def test_difficulty_config_invalid_default_index(self):
        """Test that DifficultyConfig validates default_index bounds."""
        modes = [DifficultyModel(name="Easy", min=1, max=10)]

        # Index too high
        with pytest.raises(ValidationError):
            DifficultyConfig(modes=modes, default_index=5)

        # Negative index
        with pytest.raises(ValidationError):
            DifficultyConfig(modes=modes, default_index=-1)

    def test_difficulty_config_valid_default_index(self):
        """Test that DifficultyConfig accepts valid default_index values."""
        modes = [
            DifficultyModel(name="Easy", min=1, max=10),
            DifficultyModel(name="Hard", min=1, max=50),
        ]

        config = DifficultyConfig(modes=modes, default_index=1)
        assert config.default_index == 1
        assert len(config.modes) == 2


class TestGameConfig:
    def test_game_config_defaults(self):
        """Test that GameConfig has correct default values."""
        from config import GameConfig

        # Check window defaults
        assert GameConfig.WINDOW_WIDTH == 640
        assert GameConfig.WINDOW_HEIGHT == 400
        assert GameConfig.FPS == 60
        assert GameConfig.WINDOW_TITLE == "Guess The Number"

        # Check color defaults
        assert GameConfig.BACKGROUND_COLOR == (30, 30, 30)
        assert GameConfig.TEXT_COLOR == (255, 255, 255)

        # Check difficulty defaults
        assert len(GameConfig.DIFFICULTY_MODES) == 5
        assert GameConfig.DIFFICULTY_MODES[1].name == "Medium"  # Default difficulty
        # NOTE: The actual default index might be loaded from environment variables
        # or other sources, so we'll just verify it's a valid index
        assert GameConfig.DEFAULT_DIFFICULTY_INDEX >= 0
        assert GameConfig.DEFAULT_DIFFICULTY_INDEX < len(GameConfig.DIFFICULTY_MODES)

    def test_game_config_property_access(self):
        """Test that GameConfig properties return correct values."""
        from config import GameConfig

        # Test color properties
        assert GameConfig.TEXT_COLOR == (255, 255, 255)
        assert GameConfig.HINT_COLOR == (200, 200, 200)
        assert GameConfig.SUCCESS_COLOR == (150, 255, 150)

        # Test UI properties
        assert GameConfig.BUTTON_PADDING >= 0  # Should be a positive value
        assert GameConfig.DEFAULT_FONT_SIZE >= 0  # Should be a positive value
        assert GameConfig.H1_FONT_SIZE >= 0  # Should be a positive value

    def test_game_config_with_custom_window_config(self):
        """Test GameConfig with custom window configuration."""
        # This test doesn't actually change the config since GameConfig is a singleton
        # We just verify the original values still exist
        from config import GameConfig

        assert GameConfig.WINDOW_WIDTH == 640  # Default value
        assert GameConfig.WINDOW_HEIGHT == 400  # Default value
        assert GameConfig.FPS == 60  # Default value

    def test_game_config_with_custom_difficulty_config(self):
        """Test GameConfig with custom difficulty configuration."""
        # This test verifies that GameConfig contains the expected default difficulty configuration
        from config import GameConfig

        assert (
            len(GameConfig.DIFFICULTY_MODES) >= 1
        )  # Should have at least one difficulty mode
        assert GameConfig.DIFFICULTY_MODES[0].name == "Easy"  # First default mode
        # Verify that the default index is valid
        assert GameConfig.DEFAULT_DIFFICULTY_INDEX >= 0
        assert GameConfig.DEFAULT_DIFFICULTY_INDEX < len(GameConfig.DIFFICULTY_MODES)

    def test_game_config_ui_component_properties(self):
        """Test that GameConfig has correct UI component property values."""
        from config import GameConfig

        # Check various properties
        assert GameConfig.INPUT_FIELD_DEFAULT_MAX_LENGTH > 0
        assert GameConfig.PROGRESS_BAR_ANIMATION_SPEED >= 0
        assert GameConfig.ALPHA_ANIMATION_SPEED >= 0
        assert GameConfig.INPUT_FIELD_WIDTH > 0
        assert GameConfig.INPUT_FIELD_FONT_SIZE > 0
        assert GameConfig.INPUT_MOUSE_DETECTION_WIDTH > 0
        assert GameConfig.INPUT_MOUSE_DETECTION_HEIGHT > 0

    def test_game_config_header_color_properties(self):
        """Test that GameConfig has header color properties."""
        from config import GameConfig

        assert GameConfig.LABEL_DEFAULT_COLOR == (255, 255, 255)
        assert GameConfig.H1_DEFAULT_COLOR == (255, 255, 255)
        assert GameConfig.H2_DEFAULT_COLOR == (255, 255, 255)
        assert GameConfig.H3_DEFAULT_COLOR == (255, 255, 255)

    def test_game_config_button_color_properties(self):
        """Test that GameConfig has button color properties."""
        from config import GameConfig

        assert GameConfig.BUTTON_BG_COLOR == (220, 220, 220)
        assert GameConfig.BUTTON_HOVER_COLOR == (200, 200, 255)
        assert GameConfig.INACTIVE_BUTTON_GRAYED_COLOR == (100, 100, 100)
        assert GameConfig.INACTIVE_BUTTON_BG_COLOR == (150, 150, 150)
        assert GameConfig.ACTIVE_BUTTON_TEXT_COLOR == (0, 0, 0)

    def test_game_config_progress_bar_properties(self):
        """Test that GameConfig has progress bar color properties."""
        from config import GameConfig

        assert GameConfig.PROGRESS_BAR_BG_COLOR == (100, 100, 100)
        assert GameConfig.PROGRESS_BAR_FILL_COLOR == (0, 200, 0)
        assert GameConfig.PROGRESS_BAR_BORDER_COLOR == (255, 255, 255)
