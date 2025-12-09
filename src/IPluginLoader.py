from abc import ABC, abstractmethod

from .IPlugin import IPlugin


class IPluginLoader(ABC):
    """Interface for plugin loader implementations."""

    @abstractmethod
    def load(self) -> dict[str, IPlugin]:
        """Load plugins and return mapping plugin_name -> plugin_instance.
        Implementations must never return mutable internal state; a copy
        or a new dict should be returned instead.
        """
        pass
