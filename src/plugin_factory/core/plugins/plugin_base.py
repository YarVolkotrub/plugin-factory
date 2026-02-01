from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, final

if TYPE_CHECKING:
    from plugin_factory.core import PluginInfo


class PluginBase(ABC):
    """
    Base contract for all plugins.
    """
    NAME: str
    DESCRIPTION: str | None = None

    @abstractmethod
    def initialize(self) -> None:
        """Initialize the plugin."""

    @abstractmethod
    def start(self) -> None:
        """Start the plugin."""

    @abstractmethod
    def shutdown(self) -> None:
        """Stop the plugin."""

    def __init__(self, info: PluginInfo):
        self._info = info

    @property
    def info(self) -> PluginInfo:
        return self._info

    @final
    def _apply_info(self, info: PluginInfo) -> None:
        self._info = info
