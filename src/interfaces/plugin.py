from abc import ABC, abstractmethod
from typing import ClassVar

from ..data.plugin_info import InfoBase


class PluginBase(ABC):
    """
    Base interface for all plugins.
    """

    name: ClassVar[str]

    @property
    @abstractmethod
    def info(self) -> InfoBase:
        """Prepare information about plugin."""

    @abstractmethod
    def init(self) -> None:
        """Prepare plugin (config, resources)."""

    @abstractmethod
    def start(self) -> None:
        """Start plugin work."""

    @abstractmethod
    def stop(self) -> None:
        """Stop plugin and release resources."""
