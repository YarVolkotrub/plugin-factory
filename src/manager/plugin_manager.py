from __future__ import annotations
from typing import Mapping, Callable
import logging

from ..data.plugin_state import PluginState
from ..interfaces.plugin import PluginBase
from ..data.plugin_info import InfoBase


class PluginManager:
    def __init__(self, plugins: Mapping[str, PluginBase]) -> None:
        if not plugins:
            raise ValueError("plugins mapping must not be empty")

        self.__plugins: Mapping[str, PluginBase] = plugins
        self.__states: dict[str, PluginState] = {
            name: PluginState.INIT for name in plugins
        }
        self.__errors: dict[str, str | None] = {
            name: None for name in plugins
        }

    def start(self, plugin_name: str) -> None:
        self.__execute(plugin_name, PluginBase.start, PluginState.STARTED)

    def stop(self, plugin_name: str) -> None:
        self.__execute(plugin_name, PluginBase.stop, PluginState.STOPPED)

    def start_all(self) -> dict[str, Exception | None]:
        return self.__batch(self.start)

    def stop_all(self) -> dict[str, Exception | None]:
        return self.__batch(self.stop)

    def get_info(self) -> dict[str, InfoBase | None]:
        result: dict[str, InfoBase | None] = {}

        for name, plugin in self.__plugins.items():
            try:
                result[name] = InfoBase(
                    name=name,
                    state=self.__states[name],
                    error=self.__errors[name],
                )
            except Exception:
                result[name] = None

        return result

    def get_states(self) -> dict[str, PluginState]:
        return dict(self.__states)

    def __execute(
            self,
            plugin_name: str,
            action: Callable[[PluginBase], None],
            success_state: PluginState,
    ) -> None:
        plugin = self.__get_plugin(plugin_name)

        try:
            action(plugin)
            self.__states[plugin_name] = success_state
        except Exception as exc:
            self.__states[plugin_name] = PluginState.FAILED
            self.__errors[plugin_name] = str(exc)
            logging.exception(
                "Action %s failed for plugin %s",
                action.__name__,
                plugin_name,
            )
            raise

    def __batch(
        self,
        action: Callable[[str], None],
    ) -> dict[str, Exception | None]:
        result: dict[str, Exception | None] = {}

        for name in self.__plugins:
            try:
                action(name)
                result[name] = None
            except Exception as exc:
                result[name] = exc

        return result

    def __get_plugin(self, plugin_name: str) -> PluginBase:
        if not isinstance(plugin_name, str) or not plugin_name.strip():
            raise ValueError("plugin_name must be a non-empty string")

        try:
            return self.__plugins[plugin_name]
        except KeyError:
            raise KeyError(f"Plugin not found: {plugin_name}") from None
