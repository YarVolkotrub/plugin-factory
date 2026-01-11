from __future__ import annotations

import logging
from typing import Mapping, TYPE_CHECKING

from plugin_factory.core.state_machine.plugin_action import PluginAction

if TYPE_CHECKING:
    from plugin_factory.core import PluginBase
    from plugin_factory.core import PluginInfo
    from plugin_factory.core import PluginState
    from plugin_factory.contracts import TransitionProtocol

from plugin_factory.infrastructure.state_machine.lifecycle_transitions import LifecycleTransitions


logger = logging.getLogger(__name__)

# TODO больше методов взаимодействия
class LifecycleManager:
    def __init__(self, allow_state: TransitionProtocol) -> None:
        self.__allow_state = allow_state
        self.__plugins: dict[str, PluginBase] = {}

        self.__state_transitions = LifecycleTransitions(self.__allow_state)

# region method info plugin
    def get_plugin_info(self) -> Mapping[str, PluginInfo]:
        logger.debug("Getting plugin info")
        return {name: plugin.info
                for name, plugin in self.__plugins.items()}


    def get_plugin_states(self) -> Mapping[str, PluginState]:
        logger.debug("Getting plugin states")
        return {name: plugin.info.state
                for name, plugin in self.__plugins.items()}
# endregion

# region method add plugin
    def add_plugins(self, plugins: Mapping[str, PluginBase]) -> None:
        logger.debug(
            "Adding plugins (checking duplicate): %s",
            plugins
        )
        for plugin_name in plugins.keys():
            if self.__is_plugin_exist(plugin_name):
                logger.warning(
                    "Plugin %s already exists",
                    plugin_name
                )
                return

        self.__plugins.update(plugins)

    def add_plugin_force(self, plugins: Mapping[str, PluginBase]) -> None:
        logger.debug("Adding plugins (skip duplicate): %s", plugins)
        new_plugins: Mapping[str, PluginBase] = {}

        for name, plugin in plugins.items():
            if self.__is_plugin_exist(name):
                logger.warning("Plugin %s already exists", name)
            else:
                new_plugins[name] = plugin

        self.__plugins.update(new_plugins)
# endregion

# region method for all plugin
    def init_all_plugin(self) -> None:
        logger.debug("Initializing all plugins")
        for plugin in self.__plugins.values():
            try:
                self.__change_state(PluginAction.INIT, plugin)
            except ValueError:
                ...
            except Exception as exc:
                logger.error(
                    "Failed to initialize plugin %s: %s",
                    plugin.info.name, exc
                )

    def start_all_plugin(self) ->  None:
        logger.debug("Starting all plugins")
        for plugin in self.__plugins.values():
            try:
                self.__change_state(PluginAction.START, plugin)
            except ValueError:
                ...
            except Exception as exc:
                logger.error(
                    "Failed to started plugin %s: %s",
                    plugin.info.name, exc
                )

    def stop_all_plugin(self) -> None:
        logger.debug("Stopping all plugins")
        for plugin in self.__plugins.values():
            try:
                self.__change_state(PluginAction.STOP, plugin)
            except ValueError:
                ...
            except Exception as exc:
                logger.error(
                    "Failed to stopped plugin %s: %s",
                    plugin.info.name, exc
                )
# endregion

# region method for solo plugin
    def start_plugin(self, plugin_name: str) -> None:
        logger.debug("Starting plugin: %s", plugin_name)
        plugin = self.__get_plugin(plugin_name)
        self.__change_state(PluginAction.START, plugin)

    def stop_plugin(self, plugin_name: str) -> None:
        logger.debug("Stopping plugin: %s", plugin_name)
        plugin = self.__get_plugin(plugin_name)
        self.__change_state(PluginAction.STOP, plugin)
# endregion

    def __get_plugin(self, plugin_name) -> PluginBase:
        return self.__plugins.get(plugin_name)

    def __is_plugin_exist(self, plugin_name: str) -> bool:
        logger.debug("Checking if plugin exist: %s", plugin_name)
        return plugin_name in self.__plugins

    def __change_state(self, action: PluginAction, plugin: PluginBase) -> None:
        if not self.__is_plugin_exist(plugin.info.name):
            return

        self.__state_transitions.perform_transition(plugin, action)
