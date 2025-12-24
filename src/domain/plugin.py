from __future__ import annotations
from abc import ABC, abstractmethod

from ..domain.plugin_info import PluginInfo


class PluginBase(ABC):
    """
    Base contract for all plugins.
    """

    @property
    @abstractmethod
    def info(self) -> PluginInfo: ...

    @abstractmethod
    def init(self) -> None: ...

    @abstractmethod
    def start(self) -> None: ...

    @abstractmethod
    def stop(self) -> None: ...
