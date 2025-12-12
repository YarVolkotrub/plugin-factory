from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from types import MappingProxyType

if TYPE_CHECKING:
    from .IPlugin import IPlugin


class IPluginLoader(ABC):
    @abstractmethod
    def load(self) -> MappingProxyType[str, 'IPlugin']:
        ...
