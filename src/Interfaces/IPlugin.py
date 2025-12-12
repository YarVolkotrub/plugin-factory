from abc import ABC, abstractmethod


class IPlugin(ABC):
    """Base plugin interface.

    Implementations must expose a `name` property that is unique across
    all plugins, a `status` property, and `start`/`stop` methods.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Return unique plugin name."""
        ...

    @property
    @abstractmethod
    def info(self) -> dict[str: dict]:
        ...

    @abstractmethod
    def start(self) -> None:
        """Start plugin logic."""
        ...

    @abstractmethod
    def stop(self) -> None:
        """Stop plugin logic."""
        ...
