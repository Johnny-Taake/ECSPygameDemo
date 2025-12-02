from abc import ABC, abstractmethod
from typing import Any, Callable, List

from engine import (
    BaseScene,
    EventBus,
    LabelComponent,
    ProgressBarComponent,
    ServiceLocator,
    UIBuilder,
)
from game.logic import GameLogic
from logger import get_logger

log = get_logger("game/scenes")


# NOTE: Example with lading tasks when the boot scene is entered
class LoadingTask(ABC):
    """Abstract base class for loading tasks"""

    def __init__(self, description: str):
        self.description = description

    @abstractmethod
    def execute(self) -> Any:
        """Execute the loading task and return the result"""
        pass


class SimpleTask(LoadingTask):
    """A simple task that wraps a function"""

    def __init__(self, description: str, function: Callable[[], Any]):
        super().__init__(description)
        self.function = function

    def execute(self) -> Any:
        return self.function()


# NOTE: Example asset loader with progress tracking and milestones
# ASSET LOADER
class AssetLoader:
    """Handles loading assets with progress tracking and milestones"""

    def __init__(self, frames_per_task: int = 3):
        """
        Initialize the asset loader

        Args:
            frames_per_task: Number of frames to wait before executing next task (at 60fps)
        """
        self.tasks: List[LoadingTask] = []
        self.current_task_index = 0
        self.progress = 0.0  # 0.0 to 1.0
        self.completed = False
        self.description = "Initializing..."
        self.current_task_frame_counter = 0  # Counter to control execution timing
        self.frames_per_task = frames_per_task

    def add_task(self, task: LoadingTask):
        """Add a task to be executed during asset loading"""
        self.tasks.append(task)

    def add_simple_task(self, description: str, function: Callable[[], Any]):
        """Add a simple function as a loading task"""
        self.add_task(SimpleTask(description, function))

    def add_tasks(self, tasks: List[LoadingTask]):
        """Add multiple tasks at once"""
        self.tasks.extend(tasks)

    def execute_next_task(self, dt: float):
        """Execute the next task and update progress, with frame-based timing"""
        if self.current_task_index < len(self.tasks):
            # Increment frame counter
            self.current_task_frame_counter += 1

            # Execute task only after waiting a certain number of frames
            if self.current_task_frame_counter >= self.frames_per_task:
                task = self.tasks[self.current_task_index]

                self.description = task.description
                log.info(f"AssetLoader: Executing task - {task.description}")

                # Execute the task
                task.execute()

                # Move to next task
                self.current_task_index += 1
                self.progress = self.current_task_index / len(self.tasks)

                # Reset frame counter for next task
                self.current_task_frame_counter = 0

                log.info(f"AssetLoader: Progress updated - {self.progress:.2%}")
        else:
            self.completed = True

    def reset(self):
        """Reset the loader for reuse"""
        self.current_task_index = 0
        self.progress = 0.0
        self.completed = False
        self.current_task_frame_counter = 0
        self.description = "Initializing..."


class BootScene(BaseScene):
    def __init__(self, app):
        super().__init__(app)
        self.asset_loader = AssetLoader(frames_per_task=2)  # Faster progression
        self.setup_asset_loading_tasks()
        self.loading_complete = False
        self.showing_progress = True

    def setup_asset_loading_tasks(self):
        """Define the asset loading tasks with milestones"""
        # Initialize services first (these are light initializations)
        self.asset_loader.add_simple_task(
            "Initializing services", self.initialize_services
        )

        # NOTE: Add other potential asset loading tasks here
        # For example, loading fonts, images, sounds, etc.
        self.asset_loader.add_simple_task("Loading UI assets", self.load_ui_assets)
        self.asset_loader.add_simple_task("Loading game assets", self.load_game_assets)
        self.asset_loader.add_simple_task("Loading sound assets", self.load_sound_assets)
        self.asset_loader.add_simple_task("Loading image assets", self.load_image_assets)

    def initialize_services(self):
        """Initialize services for the game"""
        event_bus = EventBus()

        ServiceLocator.provide("event_bus", event_bus)
        # Initialize game logic with default range from config
        ServiceLocator.provide(
            "game_logic", GameLogic()
        )
        log.info("Services initialized")

    def load_ui_assets(self):
        """Load UI related assets (fonts, images, etc.)"""
        try:
            # Example: Load icon or other UI assets
            icon_path = "assets/icon.png"
            # In a real implementation, you'd actually load the asset here
            # icon = pygame.image.load(icon_path)
            log.info(f"UI assets processed (e.g., {icon_path})")
        except Exception as e:
            log.warning(f"Error loading UI assets: {e}")

    def load_game_assets(self):
        """Load game specific assets"""
        try:
            # Example: Load any game-specific assets
            log.info("Game assets processed")
        except Exception as e:
            log.warning(f"Error loading game assets: {e}")

    def load_sound_assets(self):
        """Load sound assets"""
        try:
            # Get the sound system from service locator
            from engine import ServiceLocator
            sound_system = ServiceLocator.get("sound_system")

            if sound_system:
                # Load general button click sound
                sound_system.load_sound("button_click", "assets/sounds/button-click.mp3")
                # Load keyboard click sound
                sound_system.load_sound("keyboard_click", "assets/sounds/keyboard-click.mp3")
                # Load win sound
                sound_system.load_sound("win", "assets/sounds/soft-treble-win-fade-out.mp3")
                log.info("Sound assets loaded successfully")
            else:
                log.warning("Sound system not found in ServiceLocator")
        except Exception as e:
            log.warning(f"Error loading sound assets: {e}")

    def load_image_assets(self):
        """Preload image assets to cache them for later use"""
        try:
            import pygame
            # Preload the sound toggle images
            pygame.image.load("assets/images/volume.png")
            pygame.image.load("assets/images/mute.png")
            # Preload any other images that might be used
            pygame.image.load("assets/icon.png")
            log.info("Image assets preloaded successfully")
        except Exception as e:
            log.warning(f"Error preloading image assets: {e}")

    def enter(self):
        log.info("BootScene enter")

        # Create UI for loading screen
        ui = UIBuilder(self.app.font)
        self.title = ui.h1_entity("Guess The Number", 320, 150)
        self.loading_text = ui.label_entity("Initializing...", 320, 250)
        self.progress_bar = ui.progress_bar_entity(320, 300, 400, 20)

        # Add alpha components to enable fade transitions
        from engine import AlphaComponent

        self.title.add(AlphaComponent(1.0))
        self.loading_text.add(AlphaComponent(1.0))
        self.progress_bar.add(AlphaComponent(1.0))

        # Initialize entities
        self.entities = [self.title, self.loading_text, self.progress_bar]

        # Reset asset loader
        self.asset_loader.reset()

    def update(self, delta_time: float):
        # Handle fade out (inherited from BaseScene)
        # Execute next asset loading task if not completed
        if not self.asset_loader.completed:
            self.asset_loader.execute_next_task(delta_time)

            # Update progress bar component
            pb_component = self.progress_bar.get(ProgressBarComponent)
            if pb_component:
                pb_component.target_progress = self.asset_loader.progress

            # Update loading text - ensure it matches the visual progress bar
            loading_component = self.loading_text.get(LabelComponent)
            if loading_component:
                # Show actual progress percentage that matches the visual bar
                actual_percentage = int(self.asset_loader.progress * 100)
                loading_component.text = (
                    f"{self.asset_loader.description} - {actual_percentage}%"
                )

        # Check if loading is complete
        if self.asset_loader.completed and not self.loading_complete:
            self.loading_complete = True
            log.info("BootScene - All assets loaded, transitioning to menu")

            # Start fade out with callback to go to menu
            def on_fade_complete():
                from .menu import MenuScene
                self.app.scene_manager.change(MenuScene(self.app))

            self.start_fade_out(on_complete_callback=on_fade_complete)

        # Call parent update to handle fade-out if in progress
        super().update(delta_time)
