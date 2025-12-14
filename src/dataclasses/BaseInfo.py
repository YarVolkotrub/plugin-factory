from dataclasses import dataclass


@dataclass
class BaseInfo:
    """Базовая информация о плагине."""
    name: str
    state: str
    description: str = None

    def __str__(self) -> str:
        return f"{self.name}: {self.state}"
