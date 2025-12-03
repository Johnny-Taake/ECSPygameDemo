import pytest
from unittest.mock import Mock
from engine.ui_builder import UIBuilder
from engine.ecs import GameObject
from engine.components import (
    Position,
    LabelComponent,
    InputFieldComponent,
    ButtonComponent,
    H1Component,
    H2Component,
    H3Component,
    ProgressBarComponent,
    ImageComponent,
)
from config import GameConfig


class TestUIBuilder:
    @pytest.fixture
    def ui_builder(self):
        """Fixture to provide a UIBuilder instance."""
        mock_font = Mock()
        return UIBuilder(mock_font)

    def test_ui_builder_initialization(self):
        """Test that UIBuilder initializes with the provided font."""
        mock_font = Mock()
        ui_builder = UIBuilder(mock_font)
        assert ui_builder.font == mock_font

    def test_label_entity_creation(self):
        """Test that label_entity creates a GameObject with Position and LabelComponent."""
        mock_font = Mock()
        ui_builder = UIBuilder(mock_font)

        entity = ui_builder.label_entity("Test Label", 100, 200)

        # Check that the entity is created
        assert isinstance(entity, GameObject)

        # Check that Position component is added
        pos = entity.get(Position)
        assert pos is not None
        assert pos.x == 100
        assert pos.y == 200

        # Check that LabelComponent is added
        label = entity.get(LabelComponent)
        assert label is not None
        assert label.text == "Test Label"
        assert label.color == GameConfig.LABEL_DEFAULT_COLOR

    def test_label_entity_with_custom_color(self):
        """Test that label_entity accepts a custom color."""
        mock_font = Mock()
        ui_builder = UIBuilder(mock_font)

        custom_color = (255, 0, 0)
        entity = ui_builder.label_entity("Test Label", 100, 200, color=custom_color)

        label = entity.get(LabelComponent)
        assert label is not None
        assert label.color == custom_color

    def test_input_entity_creation(self):
        """Test that input_entity creates a GameObject with Position and InputFieldComponent."""
        mock_font = Mock()
        ui_builder = UIBuilder(mock_font)

        entity = ui_builder.input_entity("Enter value", 100, 200)

        # Check that the entity is created
        assert isinstance(entity, GameObject)

        # Check that Position component is added
        pos = entity.get(Position)
        assert pos is not None
        assert pos.x == 100
        assert pos.y == 200

        # Check that InputFieldComponent is added
        inp = entity.get(InputFieldComponent)
        assert inp is not None
        assert inp.placeholder == "Enter value"
        assert inp.max_length == GameConfig.INPUT_FIELD_DEFAULT_MAX_LENGTH

    def test_input_entity_with_custom_max_length(self):
        """Test that input_entity accepts a custom max_length."""
        mock_font = Mock()
        ui_builder = UIBuilder(mock_font)

        entity = ui_builder.input_entity("Enter value", 100, 200, max_len=20)

        inp = entity.get(InputFieldComponent)
        assert inp is not None
        assert inp.max_length == 20

    def test_button_entity_creation(self):
        """Test that button_entity creates a GameObject with Position and ButtonComponent."""
        mock_font = Mock()
        ui_builder = UIBuilder(mock_font)

        mock_click_handler = Mock()
        entity = ui_builder.button_entity("Click Me", 100, 200, mock_click_handler)

        # Check that the entity is created
        assert isinstance(entity, GameObject)

        # Check that Position component is added
        pos = entity.get(Position)
        assert pos is not None
        assert pos.x == 100
        assert pos.y == 200

        # Check that ButtonComponent is added
        btn = entity.get(ButtonComponent)
        assert btn is not None
        assert btn.text == "Click Me"
        assert btn.on_click == mock_click_handler
        assert btn.keyboard_shortcut is None

    def test_button_entity_with_shortcut(self):
        """Test that button_entity accepts a keyboard shortcut."""
        mock_font = Mock()
        ui_builder = UIBuilder(mock_font)

        mock_click_handler = Mock()
        entity = ui_builder.button_entity(
            "Click Me", 100, 200, mock_click_handler, "[Enter]"
        )

        btn = entity.get(ButtonComponent)
        assert btn is not None
        assert btn.keyboard_shortcut == "[Enter]"

    def test_button_entity_with_min_width(self):
        """Test that button_entity_with_min_width sets minimum width."""
        mock_font = Mock()
        ui_builder = UIBuilder(mock_font)

        mock_click_handler = Mock()
        entity = ui_builder.button_entity_with_min_width(
            "Click Me", 100, 200, mock_click_handler, 150
        )

        btn = entity.get(ButtonComponent)
        assert btn is not None
        assert btn.min_width == 150

    def test_button_entity_with_min_width_and_shortcut(self):
        """Test that button_entity_with_min_width accepts keyboard shortcut."""
        mock_font = Mock()
        ui_builder = UIBuilder(mock_font)

        mock_click_handler = Mock()
        entity = ui_builder.button_entity_with_min_width(
            "Click Me", 100, 200, mock_click_handler, 150, "[Ctrl+S]"
        )

        btn = entity.get(ButtonComponent)
        assert btn is not None
        assert btn.min_width == 150
        assert btn.keyboard_shortcut == "[Ctrl+S]"

    def test_h1_entity_creation(self):
        """Test that h1_entity creates a GameObject with Position and H1Component."""
        mock_font = Mock()
        ui_builder = UIBuilder(mock_font)

        entity = ui_builder.h1_entity("Header 1", 100, 200)

        # Check that the entity is created
        assert isinstance(entity, GameObject)

        # Check that Position component is added
        pos = entity.get(Position)
        assert pos is not None
        assert pos.x == 100
        assert pos.y == 200

        # Check that H1Component is added
        h1 = entity.get(H1Component)
        assert h1 is not None
        assert h1.text == "Header 1"
        assert h1.color == GameConfig.H1_DEFAULT_COLOR

    def test_h1_entity_with_custom_color(self):
        """Test that h1_entity accepts a custom color."""
        mock_font = Mock()
        ui_builder = UIBuilder(mock_font)

        custom_color = (255, 255, 0)
        entity = ui_builder.h1_entity("Header 1", 100, 200, color=custom_color)

        h1 = entity.get(H1Component)
        assert h1 is not None
        assert h1.color == custom_color

    def test_h2_entity_creation(self):
        """Test that h2_entity creates a GameObject with Position and H2Component."""
        mock_font = Mock()
        ui_builder = UIBuilder(mock_font)

        entity = ui_builder.h2_entity("Header 2", 100, 200)

        # Check that Position component is added
        pos = entity.get(Position)
        assert pos is not None
        assert pos.x == 100
        assert pos.y == 200

        # Check that H2Component is added
        h2 = entity.get(H2Component)
        assert h2 is not None
        assert h2.text == "Header 2"
        assert h2.color == GameConfig.H2_DEFAULT_COLOR

    def test_h3_entity_creation(self):
        """Test that h3_entity creates a GameObject with Position and H3Component."""
        mock_font = Mock()
        ui_builder = UIBuilder(mock_font)

        entity = ui_builder.h3_entity("Header 3", 100, 200)

        # Check that Position component is added
        pos = entity.get(Position)
        assert pos is not None
        assert pos.x == 100
        assert pos.y == 200

        # Check that H3Component is added
        h3 = entity.get(H3Component)
        assert h3 is not None
        assert h3.text == "Header 3"
        assert h3.color == GameConfig.H3_DEFAULT_COLOR

    def test_progress_bar_entity_creation(self):
        """Test that progress_bar_entity creates a GameObject with Position and ProgressBarComponent."""
        mock_font = Mock()
        ui_builder = UIBuilder(mock_font)

        bg_color = (100, 100, 100)
        fill_color = (0, 200, 0)
        entity = ui_builder.progress_bar_entity(
            100, 200, 200, 20, color=bg_color, fill_color=fill_color
        )

        # Check that Position component is added
        pos = entity.get(Position)
        assert pos is not None
        assert pos.x == 100
        assert pos.y == 200

        # Check that ProgressBarComponent is added
        pb = entity.get(ProgressBarComponent)
        assert pb is not None
        assert pb.x == 100
        assert pb.y == 200
        assert pb.width == 200
        assert pb.height == 20
        assert pb.color == bg_color
        assert pb.fill_color == fill_color

    def test_progress_bar_entity_with_defaults(self):
        """Test that progress_bar_entity uses default colors when none provided."""
        mock_font = Mock()
        ui_builder = UIBuilder(mock_font)

        entity = ui_builder.progress_bar_entity(100, 200, 200, 20)

        pb = entity.get(ProgressBarComponent)
        assert pb is not None
        assert pb.color == GameConfig.PROGRESS_BAR_BG_COLOR
        assert pb.fill_color == GameConfig.PROGRESS_BAR_FILL_COLOR

    def test_image_button_entity_creation(self):
        """Test that image_button_entity creates a GameObject with Position, ButtonComponent, and ImageComponent."""
        mock_font = Mock()
        ui_builder = UIBuilder(mock_font)

        mock_click_handler = Mock()
        entity = ui_builder.image_button_entity(
            "path/to/image.png", 100, 200, mock_click_handler
        )

        # Check that Position component is added
        pos = entity.get(Position)
        assert pos is not None
        assert pos.x == 100
        assert pos.y == 200

        # Check that ButtonComponent is added
        btn = entity.get(ButtonComponent)
        assert btn is not None
        assert btn.text == ""  # Image buttons have empty text
        assert btn.on_click == mock_click_handler
        assert btn.min_width == 32 + 16  # 32 is default width + 16 padding
        assert btn.min_height == 32 + 16  # 32 is default height + 16 padding

        # Check that ImageComponent is added
        img = entity.get(ImageComponent)
        assert img is not None
        assert img.image_path == "path/to/image.png"
        assert img.width == 32
        assert img.height == 32

    def test_image_button_entity_with_custom_size(self):
        """Test that image_button_entity accepts custom width and height."""
        mock_font = Mock()
        ui_builder = UIBuilder(mock_font)

        mock_click_handler = Mock()
        entity = ui_builder.image_button_entity(
            "path/to/image.png", 100, 200, mock_click_handler, width=64, height=64
        )

        btn = entity.get(ButtonComponent)
        assert btn is not None
        assert btn.min_width == 64 + 16  # Custom width + padding
        assert btn.min_height == 64 + 16  # Custom height + padding

        img = entity.get(ImageComponent)
        assert img is not None
        assert img.width == 64
        assert img.height == 64

    def test_image_button_entity_with_shortcut(self):
        """Test that image_button_entity accepts keyboard shortcut."""
        mock_font = Mock()
        ui_builder = UIBuilder(mock_font)

        mock_click_handler = Mock()
        entity = ui_builder.image_button_entity(
            "path/to/image.png",
            100,
            200,
            mock_click_handler,
            keyboard_shortcut="[Ctrl+M]",
        )

        btn = entity.get(ButtonComponent)
        assert btn is not None
        assert btn.keyboard_shortcut == "[Ctrl+M]"

    def test_all_entities_have_position_component(self):
        """Test that all entity creation methods result in entities with Position components."""
        mock_font = Mock()
        ui_builder = UIBuilder(mock_font)

        mock_click_handler = Mock()

        # Test all entity creation methods
        entities = [
            ui_builder.label_entity("Test", 10, 10),
            ui_builder.input_entity("Placeholder", 20, 20),
            ui_builder.button_entity("Button", 30, 30, mock_click_handler),
            ui_builder.h1_entity("H1", 40, 40),
            ui_builder.h2_entity("H2", 50, 50),
            ui_builder.h3_entity("H3", 60, 60),
            ui_builder.progress_bar_entity(70, 70, 100, 10),
            ui_builder.image_button_entity("path.png", 80, 80, mock_click_handler),
        ]

        # Check that all entities have Position components
        for entity in entities:
            pos = entity.get(Position)
            assert pos is not None
