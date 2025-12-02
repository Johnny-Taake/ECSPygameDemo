from .base_scene import BaseScene
from logger import get_logger

log = get_logger("engine/scene_manager")


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
