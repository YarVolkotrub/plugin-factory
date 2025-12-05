import logging
from typing import Callable

from .IPlugin import IPlugin

logger = logging.getLogger(__name__)


class PluginManager:
    def __init__(self, plugins: dict[str, IPlugin]):
        self.__plugins: dict[str, IPlugin] = plugins

    def get_status(self) -> dict[str, str]:
        statuses: dict[str, str] = {}

        for name, plugin in self.__plugins.items():
            try:
                statuses[name] = plugin.status
            except Exception:
                logger.exception("Failed to read status from plugin %s", name)
                statuses[name] = "error"

        return statuses

    def __get_plugin(self, plugin_name: str) -> IPlugin:
        plugin = self.__plugins.get(plugin_name)

        if plugin is None:
            raise KeyError(f"Plugin not found: {plugin_name}")

        return plugin

    def __execute(self, plugin_name: str,
                  action: Callable[[IPlugin], None]) -> None:
        plugin = self.__get_plugin(plugin_name)

        try:
            action(plugin)
        except Exception:
            logger.exception("Action failed for plugin %s", plugin_name)

    def start(self, plugin_name: str) -> None:
        if plugin_name is None:
            raise ValueError("plugin_name is None")

        self.__execute(plugin_name, lambda p: p.start())

    def stop(self, plugin_name: str) -> None:
        if plugin_name is None:
            raise ValueError("plugin_name is None")

        self.__execute(plugin_name, lambda p: p.stop())

    def start_all(self) -> None:
        for name in list(self.__plugins.keys()):
            try:
                self.start(name)
            except KeyError:
                logger.error("Plugin %s not found when starting all", name)

    def stop_all(self) -> None:
        for name in list(self.__plugins.keys()):
            try:
                self.stop(name)
            except KeyError:
                logger.error("Plugin %s not found when stopping all", name)
