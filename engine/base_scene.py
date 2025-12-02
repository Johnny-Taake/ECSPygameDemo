import logging

from pygame.event import Event

from .ecs import GameObject

log = logging.getLogger("engine/scenes")


class BaseScene:
    def __init__(self, app):
        self.app = app
        self.entities: list[GameObject] = []

    def enter(self):
        """Called when the scene is entered"""
        pass

    def update(self, delta_time: float):
        """Update the scene logic with delta time"""
        pass

    def exit(self):
        """Called when the scene is exited"""
        pass

    def handle_event(self, event: Event):
        """Handle events like key presses, mouse clicks, etc."""
        pass

    def render(self):
        """Render the scene - though typically handled by RenderSystem"""
        pass
