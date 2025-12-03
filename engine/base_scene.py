from pygame.event import Event

from .ecs import GameObject
from logger import get_logger

log = get_logger("engine/scenes")


class BaseScene:
    def __init__(self, app):
        self.app = app
        self.entities: list[GameObject] = []
        # Fade out variables
        self._fading_out = False
        self._fade_out_complete_callback = None

    def enter(self):
        """Called when the scene is entered"""
        pass

    def update(self, delta_time: float):
        """Update the scene logic with delta time"""
        # Handle fade out if needed
        self._handle_fade_out(delta_time)

    def exit(self):
        """Called when the scene is exited"""
        pass

    def handle_event(self, event: Event):
        """Handle events like key presses, mouse clicks, etc."""
        pass

    def update_sound_button_image(self, sounds_enabled: bool):
        """Update sound button image - default implementation does nothing.
        Override in subclasses that have sound toggle functionality."""
        pass

    def render(self):
        """Render the scene - though typically handled by RenderSystem"""
        pass

    def start_fade_out(self, target_scene=None, on_complete_callback=None):
        """
        Start the fade out animation.

        Args:
            target_scene: Optional scene to transition to when fade completes
            on_complete_callback: Optional function to call when fade out completes
        """
        from .components import AlphaComponent

        self._fading_out = True
        self._target_scene = target_scene
        self._fade_out_complete_callback = on_complete_callback

        for entity in self.entities:
            alpha_comp = entity.get(AlphaComponent)
            if alpha_comp:
                alpha_comp.target_alpha = 0.0  # Fade to transparent

    def _handle_fade_out(self, delta_time: float):
        """Handle fade out logic - checks if fade out is complete and calls callback"""
        if not self._fading_out:
            return

        # Import AlphaComponent here to avoid circular imports
        from .components import AlphaComponent

        # Check if all entities have faded out (current alpha is at or near target alpha of 0)
        all_faded = True
        for entity in self.entities:
            alpha_comp = entity.get(AlphaComponent)
            if alpha_comp:
                # Check if alpha is still above a very small threshold (close enough to 0)
                if alpha_comp.alpha > 0.01:  # Still visible, not fully faded
                    all_faded = False
                    break

        # If all entities are fully transparent, call the complete callback or change to target scene
        if all_faded:
            if self._fade_out_complete_callback:
                # Execute the callback
                self._fade_out_complete_callback()
            elif hasattr(self, '_target_scene') and self._target_scene is not None:
                # Change to the target scene if no callback was provided
                self.app.scene_manager.change(self._target_scene)
