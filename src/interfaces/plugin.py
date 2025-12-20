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
        """
        Preconditions:
            - plugin is CREATED or STOPPED
        Postconditions:
            - plugin enters INITIALIZED state
        """

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
