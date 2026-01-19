from typing import Tuple, List

from plugin_factory.core.plugins.plugin_base import PluginBase
from plugin_factory.core.plugins.plugin_instance import PluginInstance


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
