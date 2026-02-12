from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, final

if TYPE_CHECKING:
    from plugin_factory.core import PluginMetadata


class PluginBase(ABC):
    """
    Base contract for all plugins.
    Plugin must not manage lifecycle or state.
    Any exception raised will be handled by the framework.
    """
    NAME: str
    DESCRIPTION: str | None = None

    def __init__(self, info: PluginMetadata):
        self._info = info

    @property
    def info(self) -> PluginMetadata:
        """Return frozen-dataclass the plugin info."""
        return self._info

    @final
    def _apply_info(self, info: PluginMetadata) -> None:
        """The internal method for applying the plugin information
        is called only during the creation of the plugin instance
        and used by FSM"""
        self._info = info

    @abstractmethod
    def initialize(self) -> None:
        """Initialize the plugin."""

    @abstractmethod
    def start(self) -> None:
        """Start the plugin."""

    @abstractmethod
    def shutdown(self) -> None:
        """Stop the plugin."""
