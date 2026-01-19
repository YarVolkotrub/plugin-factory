from dataclasses import dataclass

from plugin_factory.core.plugins.plugin_base import PluginBase


@dataclass
class PluginInstance:
    identification: str
    instance: PluginBase
