import logging
from typing import Callable
from types import MappingProxyType

from ..interfaces.plugin import PluginBase
from ..dataclasses.info import InfoBase

logger = logging.getLogger(__name__)


class PluginManager:
    """
    Manages plugin lifecycle.

    Responsible for init, starting, stopping, and monitoring plugins.
    """

    def __init__(self, plugins: MappingProxyType[str, PluginBase]) -> None:
        self.__plugins: MappingProxyType[str, PluginBase] = plugins

    def init(self, plugin_name: str) -> None:
        if plugin_name is None:
            raise ValueError("plugin_name cannot be None")

        if not isinstance(plugin_name, str) or not plugin_name.strip():
            raise ValueError("plugin_name must be a non-empty string")

        self.__execute(plugin_name, lambda plugin: plugin.init())

    def start(self, plugin_name: str) -> None:
        if plugin_name is None:
            raise ValueError("plugin_name cannot be None")

        if not isinstance(plugin_name, str) or not plugin_name.strip():
            raise ValueError("plugin_name must be a non-empty string")

        self.__execute(plugin_name, lambda plugin: plugin.start())

    def stop(self, plugin_name: str) -> None:
        if plugin_name is None:
            raise ValueError("plugin_name cannot be None")

        if not isinstance(plugin_name, str) or not plugin_name.strip():
            raise ValueError("plugin_name must be a non-empty string")

        self.__execute(plugin_name, lambda plugin: plugin.stop())

    def start_all(self) -> None:
        for name in list(self.__plugins.keys()):
            self.start(name)

    def stop_all(self) -> None:
        for name in list(self.__plugins.keys()):
            self.stop(name)

    def get_status(self) -> dict[str, InfoBase]:
        statuses: dict[str, InfoBase] = {}

        for name, plugin in self.__plugins.items():
            try:
                statuses[name] = plugin.info
            except Exception:
                logger.exception("Failed to read status from plugin %s", name)

        return statuses

    def __get_plugin(self, plugin_name: str) -> PluginBase:
        plugin = self.__plugins.get(plugin_name)

        if plugin is None:
            raise KeyError(f"Plugin not found: {plugin_name}")

        return plugin

    def __execute(
            self,
            plugin_name: str,
            action: Callable[[PluginBase], None]
    ) -> None:
        try:
            plugin = self.__get_plugin(plugin_name)
        except KeyError as e:
            logger.error("Plugin %s not found: %s", plugin_name, e)
            return

        try:
            action(plugin)
        except Exception as exc:
            logger.exception(
                "Action failed for plugin %s: %s",
                plugin_name,
                exc
            )
