from abc import ABC, abstractmethod
from typing import ClassVar

from ..data.plugin_info import InfoBase


class PluginBase(ABC):
    """
    Base interface for all plugins.

    A plugin represents an isolated unit of functionality that can be
    dynamically discovered, loaded, started, and stopped by the system.

    Attributes:
        name: Unique plugin identifier. Must be unique across all loaded plugins.
    """

    name: ClassVar[str]

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def info(self) -> InfoBase:
        ...

    @abstractmethod
    def init(self) -> None:
        ...

    @abstractmethod
    def start(self) -> None:
        ...

    @abstractmethod
    def stop(self) -> None:
        ...
