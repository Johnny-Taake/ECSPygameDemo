from typing import Callable, Dict, List, Any
from collections import defaultdict

from logger import get_logger

log = get_logger("engine/event_bus")


class EventBus:
    def __init__(self):
        self._subs: Dict[str, List[Callable]] = defaultdict(list)

    def subscribe(self, event_name: str, callback: Callable):
        """Subscribe to an event"""
        self._subs[event_name].append(callback)

    def unsubscribe(self, event_name: str, callback: Callable):
        """Unsubscribe from an event"""
        if event_name in self._subs and callback in self._subs[event_name]:
            self._subs[event_name].remove(callback)

    def emit(self, event_name: str, data: Any = None):
        """Emit an event with optional data"""
        # NOTE: Use slice to avoid issues with callbacks that unsubscribe during emission
        for callback in self._subs[event_name][:]:
            try:
                callback(data)
            except Exception as e:
                log.exception("Error in event callback %s: %s", callback, e)
