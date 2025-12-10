from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .IPlugin import IPlugin


class IPluginLoader(ABC):
    @abstractmethod
    def load(self) -> dict[str, 'IPlugin']:
        ...
