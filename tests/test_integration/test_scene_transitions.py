import pytest
from unittest.mock import Mock, patch, MagicMock
from engine.scene_manager import SceneManager
from engine.base_scene import BaseScene
from engine.ecs import GameObject
from engine.components import AlphaComponent, Position, LabelComponent
from game.logic import GameLogic


class MockScene(BaseScene):
    """Mock scene for testing scene transitions."""

    def __init__(self, app, name="MockScene"):
        super().__init__(app)
        self.name = name
        self.enter_called = False
        self.exit_called = False
        self.event_handled = False
        self.update_called_count = 0

    def enter(self):
        self.enter_called = True

    def exit(self):
        self.exit_called = True

    def update(self, delta_time: float):
        super().update(delta_time)  # Call parent to handle fade out
        self.update_called_count += 1

    def handle_event(self, event):
        self.event_handled = True


class TestSceneManager:
    def test_scene_manager_initialization(self):
        """Test that SceneManager initializes correctly."""
        mock_app = Mock()
        scene_manager = SceneManager(mock_app)

        assert scene_manager.app == mock_app
        assert scene_manager.current is None

    def test_scene_change_initial_scene(self):
        """Test changing to the first scene."""
        mock_app = Mock()
        scene_manager = SceneManager(mock_app)

        scene = MockScene(mock_app, "TestScene")

        # Initially no scene
        assert scene_manager.current is None

        # Change to new scene
        scene_manager.change(scene)

        # Verify the scene is now current
        assert scene_manager.current == scene
        assert scene.enter_called is True
        assert scene.exit_called is False  # Should not have exited yet

    def test_scene_change_from_one_to_another(self):
        """Test changing from one scene to another."""
        mock_app = Mock()
        scene_manager = SceneManager(mock_app)

        scene1 = MockScene(mock_app, "Scene1")
        scene2 = MockScene(mock_app, "Scene2")

        # Change to first scene
        scene_manager.change(scene1)
        assert scene_manager.current == scene1
        assert scene1.enter_called is True
        assert scene1.exit_called is False

        # Change to second scene
        scene_manager.change(scene2)

        # Verify the transition
        assert scene_manager.current == scene2
        assert scene1.exit_called is True  # First scene should have been exited
        assert scene2.enter_called is True  # Second scene should have been entered

    def test_scene_change_with_exception_in_enter(self, caplog):
        """Test scene change handles exceptions in enter method."""
        mock_app = Mock()
        scene_manager = SceneManager(mock_app)

        scene1 = MockScene(mock_app, "Scene1")
        scene_manager.change(scene1)

        # Create a scene that raises an exception in enter
        class FailingScene(BaseScene):
            def enter(self):
                raise RuntimeError("Enter failed")

        failing_scene = FailingScene(mock_app)

        # This should not crash, just log the exception
        scene_manager.change(failing_scene)

        assert scene_manager.current == failing_scene

    def test_scene_change_with_exception_in_exit(self, caplog):
        """Test scene change handles exceptions in exit method."""
        mock_app = Mock()
        scene_manager = SceneManager(mock_app)

        # Create a scene that raises an exception in exit
        class FailingExitScene(BaseScene):
            def exit(self):
                raise RuntimeError("Exit failed")

            def enter(self):
                pass

        scene1 = FailingExitScene(mock_app)
        scene_manager.change(scene1)

        # Create second scene
        scene2 = MockScene(mock_app, "Scene2")

        # This should not crash when exiting the first scene, just log the exception
        scene_manager.change(scene2)

        assert scene_manager.current == scene2


class TestBaseScene:
    def test_base_scene_initialization(self):
        """Test that BaseScene initializes correctly."""
        mock_app = Mock()
        scene = BaseScene(mock_app)

        assert scene.app == mock_app
        assert scene.entities == []
        assert scene._fading_out is False
        assert scene._fade_out_complete_callback is None

    def test_base_scene_lifecycle_methods(self):
        """Test that BaseScene lifecycle methods exist and are callable."""
        mock_app = Mock()
        scene = BaseScene(mock_app)

        # These methods should exist and not raise exceptions
        scene.enter()
        scene.exit()
        scene.update(0.016)  # 1/60 seconds
        scene.handle_event(Mock())

    def test_base_scene_entities_management(self):
        """Test that BaseScene manages entities correctly."""
        mock_app = Mock()
        scene = BaseScene(mock_app)

        # Initially empty
        assert len(scene.entities) == 0

        # Add an entity
        entity = GameObject()
        scene.entities.append(entity)
        assert len(scene.entities) == 1
        assert scene.entities[0] == entity

    def test_base_scene_fade_out(self):
        """Test BaseScene fade out functionality."""
        mock_app = Mock()
        mock_app.scene_manager = Mock()
        scene = BaseScene(mock_app)

        # Add an entity with AlphaComponent
        entity = GameObject()
        entity.add(AlphaComponent(1.0))  # Fully opaque
        scene.entities.append(entity)

        # Call start_fade_out to set target alpha to 0
        callback = Mock()
        scene.start_fade_out(on_complete_callback=callback)

        # Check that fade out started
        assert scene._fading_out is True
        assert scene._fade_out_complete_callback == callback

        # Check that target alpha was set to 0 for entities with AlphaComponent
        alpha_comp = entity.get(AlphaComponent)
        assert alpha_comp is not None
        assert alpha_comp.target_alpha == 0.0

    def test_base_scene_fade_out_with_callback(self):
        """Test BaseScene fade out with callback execution."""
        mock_app = Mock()
        scene = BaseScene(mock_app)

        # Add an entity with AlphaComponent
        entity = GameObject()
        entity.add(AlphaComponent(0.01))  # Nearly transparent
        scene.entities.append(entity)

        # Set up callback
        callback = Mock()
        scene.start_fade_out(on_complete_callback=callback)

        # Simulate update that completes the fade
        scene._handle_fade_out(0.016)

        # Callback should have been called since entity is nearly transparent
        callback.assert_called_once()

    def test_update_calls_handle_fade_out(self):
        """Test that BaseScene.update calls _handle_fade_out."""
        mock_app = Mock()
        scene = BaseScene(mock_app)

        # Patch _handle_fade_out to check if it's called
        with patch.object(scene, "_handle_fade_out") as mock_handle:
            scene.update(0.016)
            mock_handle.assert_called_once_with(0.016)

    def test_update_sound_button_image_default_implementation(self):
        """Test default implementation of update_sound_button_image."""
        mock_app = Mock()
        scene = BaseScene(mock_app)

        # Should not raise exception
        scene.update_sound_button_image(True)
        scene.update_sound_button_image(False)


class TestSceneIntegration:
    def test_complete_game_flow_simulation(self):
        """Test a complete game flow with scene transitions."""
        # Mock the application
        mock_app = Mock()
        mock_app.scene_manager = SceneManager(mock_app)

        # Create mock scenes representing the game flow
        boot_scene = MockScene(mock_app, "Boot")
        menu_scene = MockScene(mock_app, "Menu")
        game_scene = MockScene(mock_app, "Game")
        win_scene = MockScene(mock_app, "Win")

        # Simulate the game flow
        mock_app.scene_manager.change(boot_scene)
        assert mock_app.scene_manager.current.name == "Boot"
        assert boot_scene.enter_called is True

        mock_app.scene_manager.change(menu_scene)
        assert mock_app.scene_manager.current.name == "Menu"
        assert boot_scene.exit_called is True
        assert menu_scene.enter_called is True

        mock_app.scene_manager.change(game_scene)
        assert mock_app.scene_manager.current.name == "Game"
        assert menu_scene.exit_called is True
        assert game_scene.enter_called is True

        mock_app.scene_manager.change(win_scene)
        assert mock_app.scene_manager.current.name == "Win"
        assert game_scene.exit_called is True
        assert win_scene.enter_called is True

    def test_game_logic_integration_with_scenes(self):
        """Test integration between GameLogic and scenes."""
        # Create a mock app
        mock_app = Mock()
        mock_app.scene_manager = Mock()

        # Create a scene
        scene = BaseScene(mock_app)

        # Test that GameLogic can be used in the scene context
        game_logic = GameLogic(min_number=1, max_number=10)
        game_logic.generate_new_number()

        # Verify game logic works independently of scene
        assert game_logic.min_number == 1
        assert game_logic.max_number == 10
        assert game_logic.number_to_guess is not None
        assert (
            game_logic.min_number <= game_logic.number_to_guess <= game_logic.max_number
        )

        # Check an invalid guess
        result = game_logic.check("invalid")
        assert result.name == "INVALID_FORMAT"

        # Reset game logic
        original_number = game_logic.number_to_guess
        game_logic.reset()
        assert game_logic.attempts == 0
        # The number should be regenerated (though might be the same value)
        assert game_logic.number_to_guess is not None

    def test_scene_with_ecs_entities(self):
        """Test a scene working with ECS entities."""
        mock_app = Mock()
        scene = BaseScene(mock_app)

        # Create entities with various components
        label_entity = GameObject()
        label_entity.add(Position(100, 100)).add(LabelComponent("Test Label"))

        alpha_entity = GameObject()
        alpha_entity.add(Position(200, 200)).add(AlphaComponent(1.0))

        # Add entities to scene
        scene.entities.extend([label_entity, alpha_entity])

        assert len(scene.entities) == 2

        # Verify entities are properly stored
        pos_comp = scene.entities[0].get(Position)
        assert pos_comp is not None
        assert pos_comp.x == 100
        assert pos_comp.y == 100

        label_comp = scene.entities[0].get(LabelComponent)
        assert label_comp is not None
        assert label_comp.text == "Test Label"

        alpha_comp = scene.entities[1].get(AlphaComponent)
        assert alpha_comp is not None
        assert alpha_comp.alpha == 1.0
