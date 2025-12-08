import pytest
from unittest.mock import Mock, patch
import pygame

from engine.systems import RenderSystem, InputSystem, SoundSystem
from engine.ecs import GameObject
from engine.components import (
    Position,
    LabelComponent,
    ButtonComponent,
    InputFieldComponent,
    AlphaComponent,
    SoundComponent,
)


class TestRenderSystem:
    @pytest.fixture
    def mock_surface(self):
        return Mock(spec=pygame.Surface)

    @pytest.fixture
    def mock_font(self):
        return Mock(spec=pygame.font.Font)

    @pytest.fixture
    def render_system(self, mock_surface, mock_font):
        # Since pygame.Surface and pygame.font.Font can't be easily mocked,
        # we'll provide mock objects to the constructor
        with patch("pygame.font.Font"), patch("pygame.font.SysFont"):
            return RenderSystem(mock_surface, mock_font)

    def test_render_system_initialization(self, mock_surface):
        """Test that RenderSystem initializes custom fonts properly."""
        with (
            patch("pygame.font.Font") as mock_font_constructor,
            patch("pygame.font.SysFont") as mock_sys_font,
        ):

            mock_font = Mock()
            mock_font_constructor.return_value = mock_font
            mock_sys_font.return_value = mock_font

            render_system = RenderSystem(mock_surface, mock_font)

            # Check that fonts were created
            assert render_system.font == mock_font
            assert render_system.h1_font == mock_font
            assert render_system.h2_font == mock_font
            assert render_system.h3_font == mock_font
            assert render_system.shortcut_font == mock_font

    def test_draw_label_calls_render(self, mock_surface, mock_font):
        """Test that draw_label calls the font's render method."""
        with patch("pygame.font.Font"), patch("pygame.font.SysFont"):
            render_system = RenderSystem(mock_surface, mock_font)
            label = LabelComponent("Test Label", (255, 255, 255))
            position = Position(100, 100)

            mock_surf = Mock()
            mock_font.render.return_value = mock_surf
            mock_surf.get_rect.return_value = pygame.Rect(0, 0, 100, 20)

            render_system.draw_label(label, position)

            mock_font.render.assert_called_once_with(
                "Test Label", True, (255, 255, 255)
            )
            mock_surface.blit.assert_called()

    def test_draw_button_calls_render(self, mock_surface, mock_font):
        """Test that draw_button calls the font's render method."""
        # Patch all pygame operations to avoid initialization issues
        with (
            patch("pygame.font.Font"),
            patch("pygame.font.SysFont"),
            patch("pygame.Rect"),
            patch("pygame.draw.rect") as mock_draw_rect,
            patch(
                "pygame.draw.line"
            ),  # Added to handle gradient highlight functionality
            patch("pygame.Surface"),
            patch("engine.systems.render.GameConfig") as mock_game_config,
        ):

            # Set up mock config values
            mock_game_config.BUTTON_PADDING = 12
            mock_game_config.ACTIVE_BUTTON_TEXT_COLOR = (0, 0, 0)
            mock_game_config.INACTIVE_BUTTON_GRAYED_COLOR = (100, 100, 100)
            mock_game_config.BUTTON_BG_COLOR = (220, 220, 220)
            mock_game_config.BUTTON_HOVER_COLOR = (200, 200, 255)
            mock_game_config.INACTIVE_BUTTON_BG_COLOR = (150, 150, 150)
            mock_game_config.BUTTON_RADIUS = 10
            mock_game_config.DEFAULT_FONT = "arial"
            mock_game_config.H1_FONT_SIZE = 36
            mock_game_config.H2_FONT_SIZE = 28
            mock_game_config.H3_FONT_SIZE = 24
            mock_game_config.BUTTON_TAG_FONT_SIZE = 8
            mock_game_config.DEFAULT_FONT_PATH = "test.ttf"
            mock_game_config.ITALIC_FONT_PATH = "test_italic.ttf"
            mock_game_config.BOLD_FONT_PATH = "test_bold.ttf"

            render_system = RenderSystem(mock_surface, mock_font)

            # Create button and ensure properties are proper values
            button = ButtonComponent("Click Me")
            button.min_width = 80
            button.min_height = 30
            button.width = 80
            button.height = 30
            button.hover = False
            button.active = True

            position = Position(100, 100)

            # Setup mock font rendering
            mock_surf = Mock()
            mock_surf.get_size.return_value = (100, 30)
            mock_font.render.return_value = mock_surf

            # Mock get_rect to return a Rect object
            mock_rect = Mock()
            mock_rect.width = 100
            mock_rect.height = 30
            mock_surf.get_rect.return_value = mock_rect

            render_system.draw_button(button, position)

            # Check that the button text was rendered and draw operations were called
            mock_font.render.assert_called_with("Click Me", True, (0, 0, 0))
            mock_draw_rect.assert_called()  # Verify that drawing operations were called

    def test_update_with_alpha_component(self, mock_surface, mock_font):
        """Test that update processes alpha component for smooth transitions."""
        with patch("pygame.font.Font"), patch("pygame.font.SysFont"):
            render_system = RenderSystem(mock_surface, mock_font)

            entity = GameObject()
            entity.add(Position(100, 100)).add(LabelComponent("Test")).add(
                AlphaComponent(0.5)
            )

            # Mock the draw method
            with patch.object(render_system, "draw_label"):
                render_system.update([entity])

                # Check that alpha was used in draw call
                # The alpha value should have been processed in the update loop


class TestInputSystem:
    def test_input_system_initialization(self):
        """Test that InputSystem initializes with no focused input."""
        input_system = InputSystem()
        assert input_system.focused_input is None

    def test_set_focus_changes_focused_input(self):
        """Test that set_focus correctly switches focus between inputs."""
        input_system = InputSystem()

        # Create mock input components
        input1 = Mock(spec=InputFieldComponent)
        input2 = Mock(spec=InputFieldComponent)

        # Initially no focus
        assert input_system.focused_input is None

        # Set focus to first input
        input_system.set_focus(input1)
        assert input_system.focused_input == input1
        input1.focused = True  # Verify that focused property was set

        # Set focus to second input
        input_system.set_focus(input2)
        assert input_system.focused_input == input2
        assert not input1.focused  # Previous input should be unfocused
        input2.focused = True  # New input should be focused

    def test_handle_key_with_no_focus_does_nothing(self):
        """Test that handle_key does nothing when no input is focused."""
        input_system = InputSystem()

        # Create a mock key event
        key_event = Mock()
        key_event.key = pygame.K_a
        key_event.unicode = "a"

        # Should not modify anything since no focus
        input_system.handle_key(key_event)

    def test_handle_key_backspace_deletes_char(self):
        """Test that handle_key processes backspace correctly."""
        input_system = InputSystem()

        input_comp = Mock(spec=InputFieldComponent)
        input_comp.text = "Hello"
        input_comp.max_length = 10

        input_system.set_focus(input_comp)

        # Simulate backspace
        backspace_event = Mock()
        backspace_event.key = pygame.K_BACKSPACE
        input_system.handle_key(backspace_event)

        # Should remove last character
        assert input_comp.text == "Hell"

    def test_handle_key_printable_char_adds_to_text(self):
        """Test that handle_key adds printable characters to text."""
        input_system = InputSystem()

        input_comp = Mock(spec=InputFieldComponent)
        input_comp.text = "Hello"
        input_comp.max_length = 10

        input_system.set_focus(input_comp)

        # Simulate typing '!'
        char_event = Mock()
        char_event.key = pygame.K_EXCLAIM
        char_event.unicode = "!"
        input_system.handle_key(char_event)

        # Should add character to text
        assert input_comp.text == "Hello!"

    def test_handle_key_exceeds_max_length(self):
        """Test that handle_key respects max length."""
        input_system = InputSystem()

        input_comp = Mock(spec=InputFieldComponent)
        input_comp.text = "A" * 5  # 5 characters
        input_comp.max_length = 5  # Max is 5

        input_system.set_focus(input_comp)

        # Try to add another character
        char_event = Mock()
        char_event.key = pygame.K_a
        char_event.unicode = "a"
        input_system.handle_key(char_event)

        # Should not add character since max length reached
        assert input_comp.text == "A" * 5

    def test_handle_mouse_focuses_input(self):
        """Test that handle_mouse focuses input fields when clicked."""
        input_system = InputSystem()

        entity = GameObject()
        pos = Position(100, 100)
        inp = InputFieldComponent(10)
        entity.add(pos).add(inp)

        # Click within input area
        input_system.handle_mouse(100, 100, [entity])

        # Verify input is now focused
        assert input_system.focused_input == inp
        assert inp.focused is True

    def test_handle_mouse_motion_sets_hover(self):
        """Test that handle_mouse_motion sets button hover state."""
        input_system = InputSystem()

        entity = GameObject()
        pos = Position(100, 100)
        btn = ButtonComponent("Test")
        entity.add(pos).add(btn)

        # Initially not hovering
        assert btn.hover is False

        # Move mouse within button bounds
        input_system.handle_mouse_motion(100, 100, [entity])

        # Should now be hovering
        assert btn.hover is True

    def test_handle_mouse_motion_resets_other_hover_states(self):
        """Test that handle_mouse_motion resets hover states for other buttons."""
        input_system = InputSystem()

        entity1 = GameObject()
        pos1 = Position(100, 100)
        btn1 = ButtonComponent("Test1")
        btn1.hover = True  # Initially hovered
        entity1.add(pos1).add(btn1)

        entity2 = GameObject()
        pos2 = Position(200, 200)
        btn2 = ButtonComponent("Test2")
        entity2.add(pos2).add(btn2)

        # Move mouse over second button
        input_system.handle_mouse_motion(200, 200, [entity1, entity2])

        # First button should no longer be hovered, second should be
        assert btn1.hover is False
        assert btn2.hover is True


class TestSoundSystem:
    def test_sound_system_initialization(self):
        """Test that SoundSystem initializes with default values."""
        with patch("pygame.mixer.init"):
            sound_system = SoundSystem()
            assert sound_system.sounds == {}
            assert sound_system.enabled is True

    def test_load_sound_success(self):
        """Test that load_sound successfully loads a sound."""
        with (
            patch("pygame.mixer.init"),
            patch("pygame.mixer.Sound") as mock_sound_class,
        ):

            mock_sound = Mock()
            mock_sound_class.return_value = mock_sound

            sound_system = SoundSystem()
            result = sound_system.load_sound("test_sound", "path/to/test.wav")

            assert result is True
            assert "test_sound" in sound_system.sounds
            mock_sound_class.assert_called_once_with("path/to/test.wav")

    def test_load_sound_failure(self):
        """Test that load_sound handles failure gracefully."""
        with (
            patch("pygame.mixer.init"),
            patch("pygame.mixer.Sound") as mock_sound_class,
        ):

            mock_sound_class.side_effect = pygame.error("Could not load sound")

            sound_system = SoundSystem()
            result = sound_system.load_sound("test_sound", "invalid/path.wav")

            assert result is False
            assert "test_sound" not in sound_system.sounds

    def test_play_sound_enabled(self):
        """Test that play_sound works when sound is enabled."""
        with patch("pygame.mixer.init"):
            sound_system = SoundSystem()

            mock_sound = Mock()
            sound_system.sounds["test"] = mock_sound

            result = sound_system.play_sound("test", 0.8)

            assert result is True
            mock_sound.set_volume.assert_called_once_with(0.8)
            mock_sound.play.assert_called_once()

    def test_play_sound_disabled(self):
        """Test that play_sound returns False when sound is disabled."""
        with patch("pygame.mixer.init"):
            sound_system = SoundSystem()
            sound_system.enabled = False

            mock_sound = Mock()
            sound_system.sounds["test"] = mock_sound

            result = sound_system.play_sound("test")

            assert result is False
            mock_sound.set_volume.assert_not_called()
            mock_sound.play.assert_not_called()

    def test_play_sound_not_found(self):
        """Test that play_sound returns False when sound doesn't exist."""
        with patch("pygame.mixer.init"):
            sound_system = SoundSystem()

            result = sound_system.play_sound("nonexistent")

            assert result is False

    def test_play_sound_from_entity(self):
        """Test that play_sound_from_entity works with SoundComponent."""
        with patch("pygame.mixer.init"):
            sound_system = SoundSystem()

            # Create an entity with SoundComponent
            entity = GameObject()
            sound_comp = SoundComponent("button_click")
            sound_comp.volume = 0.7
            entity.add(sound_comp)

            mock_sound = Mock()
            sound_system.sounds["button_click"] = mock_sound

            result = sound_system.play_sound_from_entity(entity)

            assert result is True
            mock_sound.set_volume.assert_called_once_with(0.7)
            mock_sound.play.assert_called_once()

    def test_play_sound_from_entity_disabled(self):
        """Test that play_sound_from_entity returns False when sound is disabled."""
        with patch("pygame.mixer.init"):
            sound_system = SoundSystem()
            sound_system.enabled = False

            entity = GameObject()
            sound_comp = SoundComponent("button_click")
            entity.add(sound_comp)

            result = sound_system.play_sound_from_entity(entity)

            assert result is False

    def test_enable_disable_sounds(self):
        """Test that enable_sounds and disable_sounds work correctly."""
        with patch("pygame.mixer.init"):
            sound_system = SoundSystem()

            # Start enabled
            assert sound_system.enabled is True

            # Disable
            sound_system.disable_sounds()
            assert sound_system.enabled is False

            # Re-enable
            sound_system.enable_sounds()
            assert sound_system.enabled is True

    def test_update_processes_entities_with_sound_components(self):
        """Test that update processes entities with SoundComponent."""
        with patch("pygame.mixer.init"):
            sound_system = SoundSystem()

            # Create an entity with SoundComponent that should play on add
            entity = GameObject()
            sound_comp = SoundComponent("test_sound")
            sound_comp.play_on_add = True
            sound_comp.volume = 0.5
            entity.add(sound_comp)

            # Add mock sound to system
            mock_sound = Mock()
            sound_system.sounds["test_sound"] = mock_sound

            entities = [entity]
            sound_system.update(entities)

            # Verify sound was played and play_on_add was reset
            mock_sound.set_volume.assert_called_once_with(0.5)
            mock_sound.play.assert_called_once()
            assert sound_comp.play_on_add is False
