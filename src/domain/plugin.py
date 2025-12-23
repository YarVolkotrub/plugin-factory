from __future__ import annotations

from abc import ABC, abstractmethod

from src.domain.plugin_info import PluginInfo


class PluginBase(ABC):
    """
    Base contract for all plugins.
    """

    info: PluginInfo

    @abstractmethod
    def init(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def start(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        raise NotImplementedError
