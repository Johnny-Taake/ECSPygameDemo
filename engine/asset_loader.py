"""Asset loading system for the ECS framework."""
from abc import ABC, abstractmethod
from typing import Any, Callable, List

from logger import get_logger

log = get_logger("engine/asset_loader")


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
