from .IPlugin import IPlugin

__all__: list[str] = ["IPlugin", "PLUGIN_TEMPLATE", "PLUGIN_DIR_NAME"]

PLUGIN_TEMPLATE: str = '/*/plugin*.py'
PLUGIN_DIR_NAME: str = 'plugins'
