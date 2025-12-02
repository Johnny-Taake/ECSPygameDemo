class ServiceLocator:
    _services = {}

    @classmethod
    def provide(cls, key: str, service):
        cls._services[key] = service

    @classmethod
    def get(cls, key: str):
        return cls._services.get(key)
