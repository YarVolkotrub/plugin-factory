from abc import ABC, abstractmethod


class IPlugin(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Return unique plugin name."""
        ...

    @property
    @abstractmethod
    def status(self) -> str:
        """Return plugin status."""
        ...

    @abstractmethod
    def start(self) -> None:
        """Start plugin logic."""
        ...

    @abstractmethod
    def stop(self) -> None:
        """Stop plugin logic."""
        ...
