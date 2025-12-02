import logging
from pygame.event import Event

from engine import Entity

log = logging.getLogger("engine/scene_manager")


class BaseScene:
    def __init__(self, app):
        self.app = app
        self.entities: list[Entity] = []

    def enter(self):
        pass

    def exit(self):
        pass

    def handle_event(self, event: Event):
        pass

    def update(self, dt: float):
        pass

    def render(self):
        pass


class SceneManager:
    def __init__(self, app):
        self.app = app
        self.current: BaseScene | None = None

    def change(self, new_scene: BaseScene):
        if self.current:
            try:
                self.current.exit()
            except Exception as e:
                log.exception("Error on scene exit: %s", e)
        self.current = new_scene
        log.info("scene change to %s", type(new_scene).__name__)
        try:
            self.current.enter()
        except Exception as e:
            log.exception("Error on scene enter: %s", e)
