class EventBus:
    def __init__(self):
        self._subs: dict = {}

    def subscriber(self, event_name: str, callback):
        self._subs.setdefault(event_name, []).append(callback)

    def emit(self, event_name: str, data=None):
        for cb in self._subs.get(event_name, []):
            cb(data)
