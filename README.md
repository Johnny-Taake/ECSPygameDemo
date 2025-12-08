# GuessNumberPygame

*An example of building a game with ECS + Event Bus + Responsive UI in Pygame.*

This project serves as an educational reference showing how to structure a small game professionally using Python and Pygame.
It demonstrates clean architecture, responsive UI, scenes, ECS, animations, event-driven logic, and asset pipelines.

---

## 🎥 Demo

> 🎬 **Gameplay demo:** [Watch the video](./docs/demo.mp4)

---

## ✨ What this project demonstrates

- Lightweight **ECS** (Entity–Component–System)
- **Responsive UI** with virtual resolution & letterboxing
- **Scene management** with transitions and lifecycle hooks
- **Event Bus** for decoupled communication between systems
- **Asset Loader** with progress display
- Polished **UI animations** (button press, shadows, highlight effects)
- Config system using **pydantic** / **pydantic-settings**
- Logging, error handling, and a **clean, scalable file structure**

It is a **blueprint** for beginners and intermediate developers who want to learn solid architecture on a small, understandable game.

---

## 📁 Project Structure

```text
GuessNumberPygame/
├── main.py                      # Entry point: creates GameApp and starts the game loop
│
├── build.py                     # Python helper script for building executables
├── build.spec                   # PyInstaller spec for cross-platform builds
│
├── app/
│   ├── __init__.py              # Exports application module
│   └── application.py           # GameApp class: main loop, window, responsive scaling
│
├── engine/                      # Core ECS / engine layer (framework, not game-specific)
│   ├── __init__.py              # Engine exports
│   ├── ecs.py                   # GameObject (entity) and component storage
│   ├── base_scene.py            # BaseScene class with lifecycle and fade handling
│   ├── scene_manager.py         # SceneManager: switching scenes safely
│   ├── service_locator.py       # ServiceLocator for global services (app, sound, etc.)
│   ├── event_bus.py             # EventBus: pub/sub for decoupled communication
│   ├── asset_loader.py          # AssetLoader: staged loading with progress
│   ├── ui_builder.py            # UIBuilder: factories for buttons, labels, image buttons
│   ├── components/              # ECS components
│   │   ├── __init__.py
│   │   ├── alpha.py             # AlphaComponent: fade in/out & transparency animation
│   │   ├── button.py            # ButtonComponent: text, pressed state, hover, shortcuts
│   │   ├── headers.py           # H1/H2/H3 components for semantic text styling
│   │   ├── image.py             # ImageComponent: displays images (icons, sprites)
│   │   ├── input.py             # InputFieldComponent: text input fields
│   │   ├── label.py             # LabelComponent: simple text labels
│   │   ├── position.py          # Position: x/y coordinates in virtual space
│   │   ├── progress_bar.py      # ProgressBarComponent: loading bar for boot scene
│   │   └── sound.py             # SoundComponent: describes sounds to be played
│   └── systems/                 # Systems: logic that operates on components
│       ├── __init__.py
│       ├── render.py            # RenderSystem: draws UI, buttons, text, images, animations
│       ├── input.py             # InputSystem: mouse, keyboard, focus, button press logic
│       └── sound.py             # SoundSystem: loads & plays sound effects
│
├── game/                        # Game-specific logic / scenes using the engine
│   ├── __init__.py
│   ├── logic.py                 # GameLogic: number generation, guess checking, statuses
│   └── scenes/
│       ├── __init__.py
│       ├── boot.py              # BootScene: staged asset loading with progress bar
│       ├── menu.py              # MenuScene: start game, toggle sound, etc.
│       ├── game.py              # GameScene: main gameplay (input, hints, attempts)
│       ├── win.py               # WinScene: win screen & attempts summary
│       ├── dialog.py            # DialogScene: modal overlays / messages
│       └── results_modal.py     # Results modal: highscore summary
│
├── assets/                      # All runtime assets used by the game
│   ├── fonts/                   # Custom fonts
│   │   └── *.ttf
│   ├── images/                  # Icons & UI images
│   │   ├── mute.png
│   │   └── volume.png
│   ├── sounds/                  # Sound effects
│   │   ├── button-click.mp3
│   │   ├── keyboard-click.mp3
│   │   └── soft-treble-win-fade-out.mp3
│   └── icon.png                 # Window / application icon
│
├── config/                      # Configuration system (pydantic-based)
│   ├── __init__.py
│   ├── base.py                  # Base models and shared config pieces
│   ├── game_config.py           # GameConfig: sizes, colors, FPS, UI constants
│   ├── logging.py               # Logging setup used by logger/
│   ├── settings.py              # Settings: env integration (.env, GAME_* vars)
│   └── ui.py                    # UI-specific config (padding, radii, colors)
│
├── stats/                       # Simple game statistics / persistence layer
│   ├── __init__.py
│   ├── models.py                # Stats data models
│   ├── manager.py               # Stats management logic
│   └── storage.py               # Stats persistence layer
│
├── utils/                       # Small helpers not tied to ECS
│   ├── __init__.py
│   └── responsive.py            # ResponsiveScaleManager: virtual surface + scaling
│
├── logger/                      # Logging convenience wrapper
│   ├── __init__.py              # get_logger(), setup_logging()
│   └── colored_formatter.py     # Colored log formatting
│
├── tests/                       # Tests
│
├── docs/                        # Additional documentation & guides
│   ├── UV.md                    # UV usage & command cheatsheet
│   ├── ADVANCED_ARCHITECTURE_GUIDE.md  # Deep-dive engine/architecture internals
│   └── demo.mp4                 # Gameplay demo video
│
├── .env.example                 # Example environment configuration
├── pyproject.toml               # Project dependencies and metadata (for uv/pip)
├── uv.lock                      # Resolved dependency lockfile
└── README.md                    # **THIS FILE**
````

---

## Architecture Overview

The project is intentionally structured like a mini real-world game codebase:

- **`engine/`** – reusable framework: ECS, scenes, event bus, asset loader, UI builder
- **`game/`** – game rules: number guessing, scenes for menu/game/win
- **`app/`** – application shell: Pygame window, virtual surface, main loop
- **`config/`** – configuration via pydantic, environment overrides
- **`assets/`** – all runtime assets in one place

For a deeper, maintainer-level description of internals (ECS details, scaling model, animation behavior, performance notes), see:
📄 [`docs/ADVANCED_ARCHITECTURE_GUIDE.md`](./docs/ADVANCED_ARCHITECTURE_GUIDE.md)

---

## 🧩 ECS (Entity–Component–System)

**Entities** – lightweight containers (`GameObject`)
**Components** – pure data (Position, Label, Button, Input, Image, Alpha, etc.)
**Systems** – pure logic operating on entities that have the required components.

Example: creating a UI button entity via `UIBuilder`:

```python
def button_entity(self, text: str, x: int, y: int, onclick, keyboard_shortcut: Optional[str] = None):
    e = GameObject()
    btn = ButtonComponent(text, keyboard_shortcut)
    btn.on_click = onclick
    e.add(Position(x, y)).add(btn)
    return e
```

---

## Event Bus

The **EventBus** provides a simple pub/sub mechanism so systems and scenes can react to events without direct references to each other.

```python
from engine.event_bus import event_bus

def on_play(name: str):
    sound_system.play(name)

event_bus.subscribe("sound:play", on_play)
event_bus.emit("sound:play", "click")
```

Used for:

- UI button events
- Scene transitions
- Sound triggering
- Input notifications

---

## Responsive UI (Virtual Surface + Letterboxing)

The game renders into a **fixed 640×400 virtual surface**, then:

1. Scales uniformly to fit the window
2. Adds **letterboxing** (black borders) if the aspect ratio doesn’t match
3. Converts mouse coordinates from screen → virtual space, so the logic works in a consistent coordinate system

Implemented in `utils/responsive.py`.

---

## 🎨 UI & Animation

Buttons and UI elements are designed to feel tactile:

- Shadows and depth
- Press animation (button “sinks” a few pixels on click)
- Hover / active states
- Gradient highlights

---

## 🎶 Asset Loader

Assets are loaded gradually in the **Boot Scene** with progress feedback:

- Fonts
- Images
- Sounds
- Services

`AssetLoader` executes tasks over multiple frames to avoid freezing the UI:

```python
def execute_next_task(self, dt: float):
    if self.current_task_index < len(self.tasks):
        self.current_task_frame_counter += 1
        if self.current_task_frame_counter >= self.frames_per_task:
            task = self.tasks[self.current_task_index]
            self.description = task.description
            task.execute()
            self.current_task_index += 1
            self.progress = self.current_task_index / len(self.tasks)
            self.current_task_frame_counter = 0
    else:
        self.completed = True
```

The boot scene displays a loading bar driven by `progress`.

---

## 🎮 Gameplay Summary

A simple but polished **number-guessing** game:

- Guess a random number in a configurable range (e.g. `1–N` (`N` depends on difficulty choice))
- Type your guess in an input field and submit
- The game tells you if your guess is **too low** / **too high**
- Counts attempts
- Shows a **win screen** and basic stats
- Maintains **high scores / stats** via the `stats/` module
- Navigation flow: **Menu → Game → Win** (with reset and back buttons)

Controls:

- Mouse for buttons and input focus
- Keyboard for typing numbers
- Optional hotkeys (e.g. ESC → back to menu)

---

## 📦 Installation

### Requirements

- Python **3.13+**
- [uv](https://github.com/astral-sh/uv) (optional, recommended)

### Install dependencies with uv

```bash
uv sync
```

To also install build / test / dev extras, see:
📄 [`docs/UV.md`](./docs/UV.md)

### Or install via pip

```bash
pip install -r requirements.txt
```

### Run the game

```bash
uv run main.py
```

or using venv:

```bash
python main.py
```

---

## Building Executables

Via UV:

```bash
uv sync --extra build
uv run build.py
```

Via pip and venv:

```bash
pip install -r requirements.txt
python build.py
```

Or build with the spec file using PyInstaller:

```bash
python -m PyInstaller build.spec
```

The executable bundle will be generated into the `dist/` directory.

More details:
📄 [`docs/UV.md`](./docs/UV.md)
📄 [`docs/ADVANCED_ARCHITECTURE_GUIDE.md`](./docs/ADVANCED_ARCHITECTURE_GUIDE.md)
