import logging
from engine import EventBus, ServiceLocator, BaseScene
from game.logic import GameLogic
from config import GameConfig


log = logging.getLogger("game/scenes")


class BootScene(BaseScene):
    def enter(self):
        event_bus = EventBus()
        ServiceLocator.provide("event_bus", event_bus)
        ServiceLocator.provide("game_logic", GameLogic(GameConfig.MIN_NUMBER, GameConfig.MAX_NUMBER))

        log.info("BootScene enter")

        # Import here to avoid circular imports
        from .menu import MenuScene
        self.app.scene_manager.change(MenuScene(self.app))