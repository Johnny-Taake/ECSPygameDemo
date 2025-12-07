from engine import (
    AssetLoader,
    BaseScene,
    EventBus,
    LabelComponent,
    ProgressBarComponent,
    ServiceLocator,
    UIBuilder,
)
from game.logic import GameLogic
from logger import get_logger
from utils.resources import get_resource_path

log = get_logger("game/scenes")


class BootScene(BaseScene):
    def __init__(self, app):
        super().__init__(app)
        self.asset_loader = AssetLoader(frames_per_task=2)  # Faster progression
        self.setup_asset_loading_tasks()
        self.loading_complete = False
        self.showing_progress = True

    def setup_asset_loading_tasks(self):
        """Define the asset loading tasks"""
        self.asset_loader.add_simple_task(
            "Initializing services", self.initialize_services
        )
        self.asset_loader.add_simple_task("Loading UI assets", self.load_ui_assets)
        self.asset_loader.add_simple_task("Loading game assets", self.load_game_assets)
        self.asset_loader.add_simple_task(
            "Loading sound assets", self.load_sound_assets
        )
        self.asset_loader.add_simple_task(
            "Loading image assets", self.load_image_assets
        )
        self.asset_loader.add_simple_task("Loading font assets", self.load_font_assets)

    def initialize_services(self):
        """Initialize services for the game"""
        event_bus = EventBus()

        ServiceLocator.provide("event_bus", event_bus)
        ServiceLocator.provide("game_logic", GameLogic())
        log.info("Services initialized")

    def load_ui_assets(self):
        """Load UI related assets"""
        try:
            log.info("UI assets processed (e.g., assets/icon.png)")
        except Exception as e:
            log.warning(f"Error loading UI assets: {e}")

    def load_game_assets(self):
        """Load game specific assets"""
        try:
            log.info("Game assets processed")
        except Exception as e:
            log.warning(f"Error loading game assets: {e}")

    def load_sound_assets(self):
        """Load sound assets"""
        try:
            from engine import ServiceLocator

            sound_system = ServiceLocator.get("sound_system")

            if sound_system:
                sound_system.load_sound(
                    "button_click", get_resource_path("assets/sounds/button-click.mp3")
                )
                sound_system.load_sound(
                    "keyboard_click", get_resource_path("assets/sounds/keyboard-click.mp3")
                )
                sound_system.load_sound(
                    "win", get_resource_path("assets/sounds/soft-treble-win-fade-out.mp3")
                )
                log.info("Sound assets loaded successfully")
            else:
                log.warning("Sound system not found in ServiceLocator")
        except Exception as e:
            log.warning(f"Error loading sound assets: {e}")

    def load_image_assets(self):
        """Preload image assets to cache them for later use"""
        try:
            import pygame

            pygame.image.load(get_resource_path("assets/images/volume.png"))
            pygame.image.load(get_resource_path("assets/images/mute.png"))
            pygame.image.load(get_resource_path("assets/icon.png"))
            log.info("Image assets preloaded successfully")
        except Exception as e:
            log.warning(f"Error preloading image assets: {e}")

    def load_font_assets(self):
        """Preload font assets to cache them for later use"""
        try:
            import pygame
            from config import GameConfig

            pygame.font.Font(get_resource_path(GameConfig.DEFAULT_FONT_PATH), 16)
            pygame.font.Font(get_resource_path(GameConfig.ITALIC_FONT_PATH), 16)
            pygame.font.Font(get_resource_path(GameConfig.BOLD_FONT_PATH), 16)
            log.info("Font assets preloaded successfully")
        except Exception as e:
            log.warning(f"Error preloading font assets: {e}")

    def enter(self):
        log.info("BootScene enter")

        ui = UIBuilder(self.app.font)
        self.title = ui.h1_entity("Guess The Number", 320, 150)
        self.loading_text = ui.label_entity("Initializing...", 320, 250)
        self.progress_bar = ui.progress_bar_entity(320, 300, 400, 20)

        from engine import AlphaComponent

        self.title.add(AlphaComponent(1.0))
        self.loading_text.add(AlphaComponent(1.0))
        self.progress_bar.add(AlphaComponent(1.0))

        self.entities = [self.title, self.loading_text, self.progress_bar]
        self.asset_loader.reset()

    def update(self, delta_time: float):
        if not self.asset_loader.completed:
            self.asset_loader.execute_next_task(delta_time)

            # Update progress bar component
            pb_component = self.progress_bar.get(ProgressBarComponent)
            if pb_component:
                pb_component.target_progress = self.asset_loader.progress

            # Update loading text to show actual progress
            loading_component = self.loading_text.get(LabelComponent)
            if loading_component:
                actual_percentage = int(self.asset_loader.progress * 100)
                loading_component.text = (
                    f"{self.asset_loader.description} - {actual_percentage}%"
                )

        # Check if loading is complete
        if self.asset_loader.completed and not self.loading_complete:
            self.loading_complete = True
            log.info("BootScene - All assets loaded, transitioning to menu")

            def on_fade_complete():
                from .menu import MenuScene

                self.app.scene_manager.change(MenuScene(self.app))

            self.start_fade_out(on_complete_callback=on_fade_complete)

        super().update(delta_time)
