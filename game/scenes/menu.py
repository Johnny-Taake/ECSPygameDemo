from config import GameConfig
from engine import (
    AlphaComponent,
    BaseScene,
    ButtonComponent,
    ImageComponent,
    LabelComponent,
    ServiceLocator,
    UIBuilder,
)
from engine.event_bus import EventBus
from logger import get_logger

log = get_logger("game/scenes")


class MenuScene(BaseScene):
    def enter(self):
        log.info("MenuScene enter")
        self._exit_requested = False
        self._fading_out = False

        # Get difficulty settings from configuration
        config_difficulty_modes = GameConfig.DIFFICULTY_MODES
        # Convert to the internal format expected by the code
        self.difficulty_modes = [
            {"name": mode.name, "min": mode.min, "max": mode.max}
            for mode in config_difficulty_modes
        ]

        # Get the last selected difficulty from service locator, or use default if none
        last_difficulty_raw = ServiceLocator.get("last_selected_difficulty")
        if last_difficulty_raw is not None:
            self.current_difficulty_index = last_difficulty_raw
        else:
            self.current_difficulty_index = GameConfig.DEFAULT_DIFFICULTY_INDEX

        ui = UIBuilder(self.app.font)
        self.title = ui.h1_entity("Guess The Number", 320, 60)
        self.subtitle = ui.h2_entity(
            "Press START", 320, 105, GameConfig.HINT_COLOR)

        # Difficulty selection UI
        self.difficulty_label = ui.label_entity(
            "Difficulty:", 320, 150, GameConfig.TEXT_COLOR
        )

        # Display current difficulty
        self.current_difficulty_text = ui.label_entity(
            self.get_current_difficulty_text(), 320, 175, GameConfig.TEXT_COLOR
        )

        # Left arrow for previous difficulty
        def prev_difficulty():
            self.prev_difficulty()

        difficulty_btn_center_x = 320
        btn_spacing = 60  # Space between the center and each button
        self.btn_prev = ui.button_entity(
            "<", difficulty_btn_center_x -
            btn_spacing, 220, prev_difficulty, "[<-]"
        )
        prev_component = self.btn_prev.get(ButtonComponent)
        if prev_component:
            prev_component.min_width = 100

        # Right arrow for next difficulty
        def next_difficulty():
            self.next_difficulty()

        self.btn_next = ui.button_entity(
            ">", difficulty_btn_center_x +
            btn_spacing, 220, next_difficulty, "[->]"
        )
        next_component = self.btn_next.get(ButtonComponent)
        if next_component:
            next_component.min_width = 100

        def start_game():
            self.start_game()

        # Center the start button at the exact center horizontally
        self.btn_start = ui.button_entity(
            "START", 320, 280, start_game, "[ENTER]"
        )  # Center adjusted to match other UI elements, Y position updated for proper spacing
        # Set minimum width to match the width of difficulty buttons row
        start_component = self.btn_start.get(ButtonComponent)
        if start_component:
            start_component.min_width = (
                # Same total width as difficulty buttons (100 + 20 gap + 100)
                220
            )

        def exit_game():
            self.exit_game()

        # Center the exit button at the exact center horizontally
        self.btn_exit = ui.button_entity(
            "EXIT", 320, 340, exit_game, "[ESC]"
        )  # Center adjusted to match other UI elements, Y position updated for proper spacing
        # Set minimum width to match the width of difficulty buttons row
        exit_component = self.btn_exit.get(ButtonComponent)
        if exit_component:
            exit_component.min_width = (
                # Same total width as difficulty buttons (100 + 20 gap + 100)
                220
            )

        # Sound toggle button - placed at the top right similar to the game scene
        # The button will use the global sound system state instead of its own

        def toggle_sound():
            self.toggle_sound()

        # Create the sound toggle button as an image button
        sound_btn_x = GameConfig.WINDOW_WIDTH - 50  # Same as in GameScene
        sound_btn_y = 50  # Same as in GameScene
        self.btn_sound = ui.image_button_entity(
            "assets/images/volume.png",
            sound_btn_x,
            sound_btn_y,
            toggle_sound,
            keyboard_shortcut="[Ctrl+M]",
        )

        # Set initial image based on sound system state
        sound_system = ServiceLocator.get("sound_system")
        if sound_system:
            self.update_sound_button_image(sound_system.enabled)

        # Add alpha components to enable fade transitions
        all_entities = [
            self.title,
            self.subtitle,
            self.difficulty_label,
            self.btn_prev,
            self.current_difficulty_text,
            self.btn_next,
            self.btn_start,
            self.btn_exit,
            self.btn_sound,
        ]

        for entity in all_entities:
            entity.add(AlphaComponent(1.0))

        self.entities = all_entities

    def get_current_difficulty_text(self):
        """Get text for current difficulty"""
        current = self.difficulty_modes[self.current_difficulty_index]
        return f"{current['name']}: {current['min']} - {current['max']}"

    def update_difficulty_display(self):
        """Update the difficulty display text"""
        # Update difficulty text
        difficulty_text_comp = self.current_difficulty_text.get(LabelComponent)
        if difficulty_text_comp:
            difficulty_text_comp.text = self.get_current_difficulty_text()

    def handle_event(self, event):
        import pygame

        # Check for global sound toggle (Ctrl+M)
        if event.type == pygame.KEYDOWN:
            # Global sound toggle with Ctrl+M (works in all scenes)
            if event.key == pygame.K_m and (event.mod & pygame.KMOD_CTRL):
                self.toggle_sound()

        # Handle keyboard events specific to MenuScene
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # ESC to exit
                self.exit_game()
            elif event.key == pygame.K_RETURN:  # ENTER to start game
                self.start_game()
            elif event.key == pygame.K_LEFT:  # Left arrow to decrease difficulty
                self.prev_difficulty()
            elif event.key == pygame.K_RIGHT:  # Right arrow to increase difficulty
                self.next_difficulty()

    def prev_difficulty(self):
        # Play keyboard click sound specifically for difficulty selection
        from engine import ServiceLocator

        sound_system = ServiceLocator.get("sound_system")
        if sound_system:
            sound_system.play_sound("keyboard_click")

        self.current_difficulty_index = (self.current_difficulty_index - 1) % len(
            self.difficulty_modes
        )
        self.update_difficulty_display()

    def next_difficulty(self):
        # Play keyboard click sound specifically for difficulty selection
        from engine import ServiceLocator

        sound_system = ServiceLocator.get("sound_system")
        if sound_system:
            sound_system.play_sound("keyboard_click")

        self.current_difficulty_index = (self.current_difficulty_index + 1) % len(
            self.difficulty_modes
        )
        self.update_difficulty_display()

    def start_game(self):
        log.info("Start pressed")

        # Play button click sound
        from engine import ServiceLocator

        sound_system = ServiceLocator.get("sound_system")
        if sound_system:
            sound_system.play_sound("button_click")

        # Emit difficulty event via EventBus
        event_bus = ServiceLocator.get("event_bus")
        if not isinstance(event_bus, EventBus):
            log.error("event_bus not found in ServiceLocator")
            return
        current_difficulty = self.difficulty_modes[self.current_difficulty_index]
        event_bus.emit(
            "difficulty_selected",
            {
                "min_number": current_difficulty["min"],
                "max_number": current_difficulty["max"],
                "name": current_difficulty["name"],
            },
        )

        # Update game logic in service locator with the selected difficulty as backup
        from game.logic import GameLogic

        new_game_logic = GameLogic(
            min_number=current_difficulty["min"],
            max_number=current_difficulty["max"],
        )
        ServiceLocator.provide("game_logic", new_game_logic)

        # Start fade out with callback to start the game
        def on_fade_complete():
            from .game import GameScene

            self.app.scene_manager.change(GameScene(self.app))

        self.start_fade_out(on_complete_callback=on_fade_complete)

    def exit_game(self):
        log.info("Exit pressed")

        # Play button click sound
        from engine import ServiceLocator

        sound_system = ServiceLocator.get("sound_system")
        if sound_system:
            sound_system.play_sound("button_click")

        # Start fade out with callback to exit the application
        def on_fade_complete():
            self.app.running = False

        self.start_fade_out(on_complete_callback=on_fade_complete)

    def toggle_sound(self):
        from engine import ServiceLocator

        sound_system = ServiceLocator.get("sound_system")
        if sound_system:
            # Toggle the sound system's state
            if sound_system.enabled:
                sound_system.disable_sounds()
            else:
                sound_system.enable_sounds()

            # Update the image based on the actual sound system state
            self.update_sound_button_image(sound_system.enabled)

            # Play button click sound if sound is enabled
            if sound_system.enabled:
                sound_system.play_sound("button_click")

    def update_sound_button_image(self, sounds_enabled):
        # Update the image based on the actual sound system state
        img_component = self.btn_sound.get(ImageComponent)
        if img_component:
            if sounds_enabled:
                img_component.image_path = (
                    "assets/images/volume.png"  # Unmuted icon when sounds are enabled
                )
            else:
                img_component.image_path = (
                    "assets/images/mute.png"  # Muted icon when sounds are disabled
                )
            img_component.pygame_image = None  # Reset to force reload

    def update(self, delta_time: float):
        # Call parent update to handle fade-out if in progress
        super().update(
            delta_time
        )  # This calls the BaseScene's update method which handles fade-out
