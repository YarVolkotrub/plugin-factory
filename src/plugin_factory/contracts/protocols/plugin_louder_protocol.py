from __future__ import annotations

from abc import abstractmethod
from types import MappingProxyType
from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from plugin_factory.core import PluginBase


class PluginLoaderProtocol(Protocol):
    @abstractmethod
    def load(self) -> MappingProxyType[str, PluginBase]: ...
