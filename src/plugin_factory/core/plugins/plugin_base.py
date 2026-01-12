from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plugin_factory.core import (
        PluginInfo,
        PluginState,
    )
    from plugin_factory.exceptions.exceptions import PluginError


class PluginBase(ABC):
    """
    Base contract for all plugins.
    """

    @property
    @abstractmethod
    def info(self) -> PluginInfo:
        """Get info about the plugin."""

    @info.setter
    @abstractmethod
    def info(self, value: PluginInfo) -> None:
        """Set info about the plugin."""

    @abstractmethod
    def initialize(self) -> None:
        """Initialize the plugin."""

    @abstractmethod
    def start(self) -> None:
        """Start the plugin."""

    @abstractmethod
    def shutdown(self) -> None:
        """Stop the plugin."""

    def set_state(self, new_state: PluginState) -> None:
        """Set the state of the plugin."""
        self.info = self.info.switch_state(new_state)

    def set_error(self, new_error: PluginError) -> None:
        """Set the error of the plugin."""
        self.info = self.info.set_error(new_error)
