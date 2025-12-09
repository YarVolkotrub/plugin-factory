from .IPlugin import IPlugin
from .IPluginLoader import IPluginLoader
from .plugin_manager import PluginManager

__all__ = [
    "IPlugin",
    "IPluginLoader",
    "PluginManager",
    "PLUGIN_TEMPLATE",
    "PLUGIN_DIR_NAME"
]


PLUGIN_TEMPLATE: str = '/*/plugin*.py'
PLUGIN_DIR_NAME: str = 'plugins'
