import os
import sys
import pygame
import pytest
from unittest.mock import Mock, patch

# Add the project root directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config import GameConfig
from engine.ecs import GameObject
from game.logic import GameLogic


@pytest.fixture
def game_config():
    """Fixture to provide a game configuration instance."""
    return GameConfig


@pytest.fixture
def game_object():
    """Fixture to provide a basic GameObject instance."""
    return GameObject()


@pytest.fixture
def mock_pygame_surface():
    """Fixture to provide a mock pygame surface."""
    with patch("pygame.Surface") as mock_surface:
        yield mock_surface


@pytest.fixture
def mock_pygame_font():
    """Fixture to provide a mock pygame font."""
    with patch("pygame.font.Font") as mock_font:
        mock_font_instance = Mock()
        mock_font_instance.render.return_value = Mock()
        mock_font.return_value = mock_font_instance
        yield mock_font_instance


@pytest.fixture
def game_logic():
    """Fixture to provide a GameLogic instance with default parameters."""
    return GameLogic(min_number=1, max_number=100)


@pytest.fixture
def game_logic_easy():
    """Fixture to provide a GameLogic instance with easy difficulty."""
    return GameLogic(min_number=1, max_number=10)


@pytest.fixture
def game_logic_medium():
    """Fixture to provide a GameLogic instance with medium difficulty."""
    return GameLogic(min_number=1, max_number=100)


@pytest.fixture
def game_logic_hard():
    """Fixture to provide a GameLogic instance with hard difficulty."""
    return GameLogic(min_number=1, max_number=1000)


@pytest.fixture
def mock_service_locator():
    """Fixture to provide a mock service locator."""
    with patch("engine.service_locator.ServiceLocator") as mock:
        yield mock


@pytest.fixture
def mock_event_bus():
    """Fixture to provide a mock event bus."""
    with patch("engine.event_bus.EventBus") as mock_event_bus:
        yield mock_event_bus


@pytest.fixture
def setup_pygame():
    """Fixture to set up pygame for testing."""
    # Initialize pygame in a controlled way for tests
    pygame.init()
    yield
    pygame.quit()
