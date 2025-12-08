"""Unit tests for extended resource loading utilities."""

from unittest.mock import patch, Mock
from utils.resources_extended import (
    load_font_with_fallback,
    load_image_with_fallback,
    load_sound_with_fallback,
)


class TestLoadFontWithFallback:
    """Test the load_font_with_fallback function."""

    @patch("utils.resources_extended.get_resource_path")
    @patch("utils.resources_extended.pygame")
    def test_load_font_with_fallback_success(self, mock_pygame, mock_get_resource_path):
        """Test loading font successfully."""
        mock_get_resource_path.return_value = "/path/to/font.ttf"
        mock_font_instance = Mock()
        mock_pygame.font.Font.return_value = mock_font_instance

        result = load_font_with_fallback(16, "assets/fonts/test.ttf")

        mock_get_resource_path.assert_called_once_with("assets/fonts/test.ttf")
        mock_pygame.font.Font.assert_called_once_with("/path/to/font.ttf", 16)
        assert result == mock_font_instance

    @patch("utils.resources_extended.get_resource_path")
    @patch("utils.resources_extended.pygame")
    def test_load_font_with_fallback_file_not_found(
        self, mock_pygame, mock_get_resource_path
    ):
        """Test font loading with fallback when file is not found."""
        mock_get_resource_path.return_value = "/path/to/missing.ttf"
        mock_pygame.font.Font.side_effect = FileNotFoundError("Font file not found")
        mock_fallback_font = Mock()
        mock_pygame.font.SysFont.return_value = mock_fallback_font

        from config import GameConfig

        result = load_font_with_fallback(16, "assets/fonts/missing.ttf")

        mock_get_resource_path.assert_called_once_with("assets/fonts/missing.ttf")
        mock_pygame.font.SysFont.assert_called_once_with(GameConfig.DEFAULT_FONT, 16)
        assert result == mock_fallback_font

    @patch("utils.resources_extended.get_resource_path")
    @patch("utils.resources_extended.pygame")
    def test_load_font_with_fallback_pygame_error(
        self, mock_pygame, mock_get_resource_path
    ):
        """Test font loading with fallback when pygame throws an error."""
        mock_get_resource_path.return_value = "/path/to/corrupted.ttf"
        mock_pygame.font.Font.side_effect = Exception("Could not load font")
        mock_fallback_font = Mock()
        mock_pygame.font.SysFont.return_value = mock_fallback_font

        from config import GameConfig

        result = load_font_with_fallback(16, "assets/fonts/corrupted.ttf")

        mock_get_resource_path.assert_called_once_with("assets/fonts/corrupted.ttf")
        mock_pygame.font.SysFont.assert_called_once_with(GameConfig.DEFAULT_FONT, 16)
        assert result == mock_fallback_font

    @patch("utils.resources_extended.get_resource_path")
    @patch("utils.resources_extended.pygame")
    def test_load_font_with_fallback_default_path(
        self, mock_pygame, mock_get_resource_path
    ):
        """Test font loading with default path."""
        from config import GameConfig

        mock_get_resource_path.return_value = "/path/to/default.ttf"
        mock_font_instance = Mock()
        mock_pygame.font.Font.return_value = mock_font_instance

        result = load_font_with_fallback(12)  # Should use default font path

        mock_get_resource_path.assert_called_once_with(GameConfig.DEFAULT_FONT_PATH)
        mock_pygame.font.Font.assert_called_once_with("/path/to/default.ttf", 12)
        assert result == mock_font_instance


class TestLoadImageWithFallback:
    """Test the load_image_with_fallback function."""

    @patch("utils.resources_extended.get_resource_path")
    @patch("utils.resources_extended.pygame")
    def test_load_image_with_fallback_success(
        self, mock_pygame, mock_get_resource_path
    ):
        """Test loading image successfully."""
        mock_get_resource_path.return_value = "/path/to/image.png"
        mock_loaded_image = Mock()
        mock_transformed_image = Mock()
        mock_pygame.image.load.return_value.convert_alpha.return_value = (
            mock_loaded_image
        )
        mock_pygame.transform.scale.return_value = mock_transformed_image

        # Test with dimensions
        result = load_image_with_fallback("assets/images/test.png", 100, 50)

        mock_get_resource_path.assert_called_once_with("assets/images/test.png")
        mock_pygame.image.load.assert_called_once_with("/path/to/image.png")
        mock_pygame.transform.scale.assert_called_once_with(
            mock_loaded_image, (100, 50)
        )
        assert result == mock_transformed_image

    @patch("utils.resources_extended.get_resource_path")
    @patch("utils.resources_extended.pygame")
    def test_load_image_with_fallback_success_no_resize(
        self, mock_pygame, mock_get_resource_path
    ):
        """Test loading image successfully without resizing."""
        mock_get_resource_path.return_value = "/path/to/image.png"
        mock_loaded_image = Mock()
        mock_pygame.image.load.return_value.convert_alpha.return_value = (
            mock_loaded_image
        )

        # Test without dimensions
        result = load_image_with_fallback("assets/images/test.png")

        mock_get_resource_path.assert_called_once_with("assets/images/test.png")
        mock_pygame.image.load.assert_called_once_with("/path/to/image.png")
        assert result == mock_loaded_image

    @patch("utils.resources_extended.get_resource_path")
    @patch("utils.resources_extended.pygame")
    def test_load_image_with_fallback_error_returns_placeholder(
        self, mock_pygame, mock_get_resource_path
    ):
        """Test that image loading returns placeholder when pygame throws an error."""
        mock_get_resource_path.return_value = "/path/to/missing.png"
        mock_pygame.image.load.side_effect = Exception("Could not load image")

        # Mock pygame stuff for the placeholder
        mock_placeholder = Mock()
        mock_pygame.Surface.return_value = mock_placeholder
        mock_pygame.Rect = Mock()

        result = load_image_with_fallback("assets/images/missing.png", 64, 64)

        mock_get_resource_path.assert_called_once_with("assets/images/missing.png")
        mock_pygame.Surface.assert_called()
        assert result == mock_placeholder


class TestLoadSoundWithFallback:
    """Test the load_sound_with_fallback function."""

    @patch("utils.resources_extended.get_resource_path")
    @patch("utils.resources_extended.pygame")
    def test_load_sound_with_fallback_success(
        self, mock_pygame, mock_get_resource_path
    ):
        """Test loading sound successfully."""
        mock_get_resource_path.return_value = "/path/to/sound.mp3"
        mock_sound_instance = Mock()
        mock_pygame.mixer.Sound.return_value = mock_sound_instance

        result = load_sound_with_fallback("assets/sounds/test.mp3", "test_sound")

        mock_get_resource_path.assert_called_once_with("assets/sounds/test.mp3")
        mock_pygame.mixer.Sound.assert_called_once_with("/path/to/sound.mp3")
        assert result == mock_sound_instance

    @patch("utils.resources_extended.get_resource_path")
    @patch("utils.resources_extended.pygame")
    def test_load_sound_with_fallback_without_name(
        self, mock_pygame, mock_get_resource_path
    ):
        """Test loading sound without specifying name."""
        mock_get_resource_path.return_value = "/path/to/sound.mp3"
        mock_sound_instance = Mock()
        mock_pygame.mixer.Sound.return_value = mock_sound_instance

        result = load_sound_with_fallback("assets/sounds/test.mp3")

        mock_get_resource_path.assert_called_once_with("assets/sounds/test.mp3")
        mock_pygame.mixer.Sound.assert_called_once_with("/path/to/sound.mp3")
        assert result == mock_sound_instance

    @patch("utils.resources_extended.get_resource_path")
    @patch("utils.resources_extended.pygame")
    def test_load_sound_with_fallback_error_returns_none(
        self, mock_pygame, mock_get_resource_path
    ):
        """Test that sound loading returns None when pygame throws an error."""
        mock_get_resource_path.return_value = "/path/to/missing.mp3"
        mock_pygame.mixer.Sound.side_effect = Exception("Could not load sound")

        result = load_sound_with_fallback("assets/sounds/missing.mp3", "missing_sound")

        mock_get_resource_path.assert_called_once_with("assets/sounds/missing.mp3")
        assert result is None
