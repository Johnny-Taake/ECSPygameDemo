# Testing Guide

## Testing Overview

The project uses `pytest` for testing and includes various types of tests to ensure code quality:

- **Unit Tests**: Test individual components and utilities
- **Integration Tests**: Test how different systems work together
- **Configuration Tests**: Test configuration validation and loading

---

## Test Structure

```sh
tests/
├── test_components/       # ECS component tests
│   └── test_components.py
├── test_config/           # Configuration model tests
│   └── test_config.py
├── test_engine/           # Engine layer tests
│   └── test_ui_builder.py
├── test_game/             # Game logic tests
│   └── test_game_logic.py
├── test_integration/      # Integration tests
│   └── test_scene_transitions.py
├── test_systems/          # ECS system tests
│   └── test_systems.py
├── test_utils/            # Utility function tests
│   ├── test_graphics.py
│   ├── test_helpers.py
│   ├── test_resources_extended.py
│   └── test_responsive.py
└── conftest.py            # Test fixtures and configuration
```

---

## Running Tests

### With uv (recommended)

```bash
# Run all tests
uv run --extra test pytest

# Run tests with coverage
# View coverage report in `htmlcov/index.html`. You can serve this report with `python -m http.server`.
uv run --extra test pytest --cov=app --cov=config --cov=engine --cov=game --cov=utils --cov=logger --cov-report=html

# Run specific test file
uv run --extra test pytest tests/test_game/test_game_logic.py

# Run with verbose output
uv run --extra test pytest -v
```

### With pip/venv

First activate your virtual environment, then:

```bash
# Run all tests
pytest

# Run with coverage
# View coverage report in `htmlcov/index.html`. You can serve this report with `python -m http.server`.
pytest --cov=app --cov=config --cov=engine --cov=game --cov=utils --cov=logger --cov-report=html

```
