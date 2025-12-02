import logging

from engine import BaseScene, ButtonComponent, UIBuilder, AlphaComponent
from config import GameConfig


log = logging.getLogger("game/scenes")


class DialogScene(BaseScene):
    def __init__(self, app, title: str, message: str, on_confirm, on_cancel=None, confirm_text: str = "Yes", cancel_text: str = "No"):
        super().__init__(app)
        self.title_text = title
        self.message = message
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        self.confirm_text = confirm_text
        self.cancel_text = cancel_text
        self.previous_scene = None

    def enter(self):
        log.info("DialogScene enter")
        ui = UIBuilder(self.app.font)

        # Create a semi-transparent background overlay
        overlay_entity = ui.label_entity("", 320, 240)
        overlay_entity.add(AlphaComponent(0.5))  # Semi-transparent overlay

        # Dialog title
        self.title = ui.h2_entity(self.title_text, 320, 180, GameConfig.TEXT_COLOR)

        # Dialog message
        self.message_label = ui.label_entity(self.message, 320, 220, GameConfig.TEXT_COLOR)

        # Confirmation button
        def confirm():
            log.info("Dialog confirm")
            # Execute the confirm callback
            self.on_confirm()
        # Cancel button
        def cancel():
            log.info("Dialog cancel")
            if self.on_cancel is not None:
                self.on_cancel()
            else:
                # If no cancel callback is provided, go back to previous scene
                if self.previous_scene is not None:
                    self.app.scene_manager.change(self.previous_scene)
                else:
                    # Fallback behavior
                    from .menu import MenuScene
                    self.app.scene_manager.change(MenuScene(self.app))

        # Position buttons with appropriate spacing
        self.btn_confirm = ui.button_entity(self.confirm_text, 250, 270, confirm)
        self.btn_cancel = ui.button_entity(self.cancel_text, 400, 270, cancel)

        # Set minimum width to match
        confirm_component = self.btn_confirm.get(ButtonComponent)
        cancel_component = self.btn_cancel.get(ButtonComponent)
        if confirm_component:
            confirm_component.min_width = 100
        if cancel_component:
            cancel_component.min_width = 100

        # Add alpha components for fade transition
        for entity in [self.title, self.message_label, self.btn_confirm, self.btn_cancel, overlay_entity]:
            entity.add(AlphaComponent(1.0))

        self.entities = [
            overlay_entity,
            self.title,
            self.message_label,
            self.btn_confirm,
            self.btn_cancel
        ]

    def update(self, delta_time: float):
        # Handle fade out if needed (when confirming)
        if hasattr(self, '_fading_out') and self._fading_out:
            # Check if all entities have faded out (current alpha is at or near target alpha of 0)
            all_faded = True
            for entity in self.entities:
                alpha_comp = entity.get(AlphaComponent)
                if alpha_comp:
                    # Check if alpha is still above a very small threshold (close enough to 0)
                    if alpha_comp.alpha > 0.01:  # Still visible, not fully faded
                        all_faded = False
                        break

            # If all entities are fully transparent, transition to the target scene
            if all_faded:
                if hasattr(self, '_target_scene') and self._target_scene is not None:
                    self.app.scene_manager.change(self._target_scene)
                else:
                    # If no target scene was defined, return to the previous scene
                    if hasattr(self, 'previous_scene') and self.previous_scene is not None:
                        self.app.scene_manager.change(self.previous_scene)

    def start_fade_out(self, target_scene=None):
        """Start the fade out animation before transitioning to the next scene"""
        self._fading_out = True
        if target_scene:
            self._target_scene = target_scene
        for entity in self.entities:
            alpha_comp = entity.get(AlphaComponent)
            if alpha_comp:
                alpha_comp.target_alpha = 0.0  # Fade to transparent
