from typing import Any, Dict, Optional


class ServiceLocator:
    _services: Dict[str, Any] = {}

    @classmethod
    def provide(cls, key: str, service: Any) -> None:
        cls._services[key] = service

    @classmethod
    def get(cls, key: str) -> Optional[Any]:
        return cls._services.get(key)
