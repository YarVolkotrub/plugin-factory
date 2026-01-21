from __future__ import annotations

from typing import Tuple, List, TYPE_CHECKING, Dict
from types import MappingProxyType

from plugin_factory.core import PluginInstance

if TYPE_CHECKING:
    from plugin_factory.core import PluginBase

class PluginRegistry:
    def __init__(self):
        self.__plugins: Dict[PluginInstance.identifier, PluginInstance.instance] = {}

    @property
    def plugins(self):
        return MappingProxyType(self.__plugins)

    def register(self, plugin: PluginBase) -> None:
        self.__plugins[plugin.info.name] = plugin

    def __len__(self) -> int:
        return len(self.__plugins)

    def __iter__(self):
        return iter(self.__plugins)
