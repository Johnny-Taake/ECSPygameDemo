from engine.components import (
    Position,
    LabelComponent,
    ButtonComponent,
    InputFieldComponent,
    H1Component,
    H2Component,
    H3Component,
    AlphaComponent,
    ProgressBarComponent,
    ImageComponent,
    SoundComponent,
)


class TestPosition:
    def test_position_initialization(self):
        """Test that Position component is properly initialized."""
        pos = Position(10, 20)
        assert pos.x == 10
        assert pos.y == 20

    def test_position_values_different(self):
        """Test that Position can handle different x and y values."""
        pos = Position(100, -50)
        assert pos.x == 100
        assert pos.y == -50

    def test_position_zero_values(self):
        """Test that Position works with zero values."""
        pos = Position(0, 0)
        assert pos.x == 0
        assert pos.y == 0


class TestLabelComponent:
    def test_label_initialization(self):
        """Test that LabelComponent is properly initialized."""
        label = LabelComponent("Hello World")
        assert label.text == "Hello World"

    def test_label_with_color(self):
        """Test that LabelComponent accepts and stores color."""
        color = (255, 0, 0)
        label = LabelComponent("Test", color)
        assert label.color == color

    def test_label_default_color(self):
        """Test that LabelComponent uses default color when none provided."""
        from config import GameConfig

        label = LabelComponent("Test")
        assert label.color == GameConfig.LABEL_DEFAULT_COLOR


class TestButtonComponent:
    def test_button_initialization(self):
        """Test that ButtonComponent is properly initialized."""
        button = ButtonComponent("Click Me")
        assert button.text == "Click Me"
        assert button.on_click is None
        assert button.hover is False
        assert button.active is True

    def test_button_with_shortcut(self):
        """Test that ButtonComponent accepts keyboard shortcut."""
        button = ButtonComponent("Test", "[Enter]")
        assert button.text == "Test"
        assert button.keyboard_shortcut == "[Enter]"

    def test_button_defaults(self):
        """Test that ButtonComponent has proper default values."""
        button = ButtonComponent("Test")
        assert button.width == 0
        assert button.height == 0
        assert button.min_width == 0
        assert button.min_height == 0
        assert button.active is True
        assert button.hover is False

    def test_button_set_properties(self):
        """Test that ButtonComponent properties can be modified."""
        button = ButtonComponent("Test")
        button.width = 100
        button.height = 50
        button.min_width = 80
        button.min_height = 40
        button.hover = True
        button.active = False

        assert button.width == 100
        assert button.height == 50
        assert button.min_width == 80
        assert button.min_height == 40
        assert button.hover is True
        assert button.active is False


class TestInputFieldComponent:
    def test_input_field_initialization(self):
        """Test that InputFieldComponent is properly initialized."""
        input_field = InputFieldComponent(10)  # max length of 10
        assert input_field.max_length == 10
        assert input_field.text == ""
        assert input_field.focused is False
        assert input_field.placeholder == ""

    def test_input_field_with_placeholder(self):
        """Test that InputFieldComponent can have a placeholder."""
        input_field = InputFieldComponent(5)
        input_field.placeholder = "Enter number"
        assert input_field.placeholder == "Enter number"

    def test_input_field_text_modification(self):
        """Test that InputFieldComponent text can be modified."""
        input_field = InputFieldComponent(10)
        input_field.text = "Hello"
        assert input_field.text == "Hello"

    def test_input_field_focused(self):
        """Test that InputFieldComponent focused state can be set."""
        input_field = InputFieldComponent(10)
        input_field.focused = True
        assert input_field.focused is True


class TestHeaderComponents:
    def test_h1_component(self):
        """Test H1Component initialization."""
        h1 = H1Component("Title", (255, 255, 255))
        assert h1.text == "Title"
        assert h1.color == (255, 255, 255)

    def test_h2_component(self):
        """Test H2Component initialization."""
        h2 = H2Component("Subtitle", (200, 200, 200))
        assert h2.text == "Subtitle"
        assert h2.color == (200, 200, 200)

    def test_h3_component(self):
        """Test H3Component initialization."""
        h3 = H3Component("Section", (150, 150, 150))
        assert h3.text == "Section"
        assert h3.color == (150, 150, 150)


class TestAlphaComponent:
    def test_alpha_component_initialization(self):
        """Test AlphaComponent initialization."""
        alpha = AlphaComponent(0.5)
        assert alpha.alpha == 0.5
        assert alpha.target_alpha == 0.5

    def test_alpha_component_defaults(self):
        """Test AlphaComponent default values."""
        alpha = AlphaComponent(1.0)
        assert alpha.alpha == 1.0
        assert alpha.target_alpha == 1.0
        # Check that animation_speed exists (value depends on GameConfig)
        assert hasattr(alpha, "animation_speed")

    def test_alpha_component_custom_values(self):
        """Test AlphaComponent with different initial alpha value."""
        alpha = AlphaComponent(0.5)
        assert alpha.alpha == 0.5
        assert alpha.target_alpha == 0.5
        # Check that animation_speed exists
        assert hasattr(alpha, "animation_speed")


class TestProgressBarComponent:
    def test_progress_bar_initialization(self):
        """Test ProgressBarComponent initialization."""
        pb = ProgressBarComponent(100, 100, 200, 30)
        assert pb.x == 100
        assert pb.y == 100
        assert pb.width == 200
        assert pb.height == 30
        assert pb.progress == 0.0
        assert pb.target_progress == 0.0

    def test_progress_bar_with_colors(self):
        """Test ProgressBarComponent with custom colors."""
        bg_color = (50, 50, 50)
        fill_color = (100, 200, 100)
        pb = ProgressBarComponent(0, 0, 100, 20, bg_color, fill_color)
        assert pb.color == bg_color
        assert pb.fill_color == fill_color

    def test_progress_bar_progress_update(self):
        """Test ProgressBarComponent progress can be updated."""
        pb = ProgressBarComponent(0, 0, 100, 20)
        pb.target_progress = 0.75
        assert pb.target_progress == 0.75


class TestImageComponent:
    def test_image_component_initialization(self):
        """Test ImageComponent initialization."""
        img = ImageComponent("path/to/image.png", 64, 64)
        assert img.image_path == "path/to/image.png"
        assert img.width == 64
        assert img.height == 64
        assert img.pygame_image is None

    def test_image_component_properties(self):
        """Test ImageComponent properties."""
        img = ImageComponent("test.jpg", 128, 128)
        assert img.image_path == "test.jpg"
        assert img.width == 128
        assert img.height == 128


class TestSoundComponent:
    def test_sound_component_initialization(self):
        """Test SoundComponent initialization."""
        sound = SoundComponent("button_click")
        assert sound.sound_name == "button_click"
        assert sound.play_on_add is False
        assert sound.volume == 1.0
        assert sound.loop is False

    def test_sound_component_with_parameters(self):
        """Test SoundComponent with custom parameters."""
        sound = SoundComponent("test_sound")
        sound.play_on_add = True
        sound.volume = 0.5
        sound.loop = True

        assert sound.play_on_add is True
        assert sound.volume == 0.5
        assert sound.loop is True
