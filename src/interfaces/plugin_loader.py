from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from types import MappingProxyType

if TYPE_CHECKING:
    from .plugin import PluginBase


class PluginLoaderBase(ABC):
    """
    Resolves import paths for locally stored plugins.
    """

    @abstractmethod
    def load(self) -> MappingProxyType[str, 'PluginBase']:
        ...
