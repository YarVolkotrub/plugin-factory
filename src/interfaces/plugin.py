from abc import ABC, abstractmethod
from typing import ClassVar

from ..data.plugin_info import PluginInfo


class PluginBase(ABC):
    """
    Base interface for all plugins.
    """

    name: ClassVar[str]

    @property
    @abstractmethod
    def info(self) -> PluginInfo:
        """Prepare information about plugin."""

    @abstractmethod
    def init(self) -> None:
        """
        Prepare plugin for execution.

        Preconditions:
            - plugin is CREATED or STOPPED
        Postconditions:
            - plugin enters INITIALIZED state
        """

        raise NotImplementedError

    @abstractmethod
    def start(self) -> None:
        """
        Preconditions:
            - plugin is INITIALIZED
        Postconditions:
            - plugin enters RUNNING state
        """

    @abstractmethod
    def stop(self) -> None:
        """
        Preconditions:
            - plugin is RUNNING
        Postconditions:
            - plugin enters STOPPING state
        """
