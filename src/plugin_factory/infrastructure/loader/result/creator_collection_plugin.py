from __future__ import annotations

from typing import Tuple, List, TYPE_CHECKING

from plugin_factory.core import PluginInstance

if TYPE_CHECKING:
    from plugin_factory.core import PluginBase

class CreatorCollectionPlugin:
    def __init__(self):
        self.__plugins: List[PluginInstance] = []

    @property
    def plugins(self) -> Tuple[PluginInstance, ...]:
        return tuple(self.__plugins)

    def add_plugin(self, plugin: PluginBase) -> None:
        self.__plugins.append(
            PluginInstance(
                identification=plugin.info.name,
                instance=plugin,
            )
        )

    def __len__(self) -> int:
        return len(self.__plugins)
