from __future__ import annotations

import logging
from types import MappingProxyType
from typing import Mapping, TYPE_CHECKING, Dict

from plugin_factory.core import FSMAction
from plugin_factory.exceptions import PluginStateError
from plugin_factory.infrastructure.state_machine.lifecycle_transitions import \
    LifecycleTransitions

if TYPE_CHECKING:
    from plugin_factory.core import (
        PluginBase,
        PluginInfo,
        FSMState
    )


logger = logging.getLogger(__name__)

# TODO больше методов взаимодействия
class LifecycleManager:
    def __init__(self, allow_state: MappingProxyType[
        FSMState,Dict[FSMAction, FSMState]
    ]) -> None:
        self._plugins: Dict[str, PluginBase] = {}
        self._state_transitions = LifecycleTransitions(allow_state)

# region Plugin Information Methods
    def get_plugin_info(self) -> Mapping[str, PluginInfo]:
        logger.debug("Getting plugin info")
        return {name: plugin.info
                for name, plugin in self._plugins.items()}

    def get_plugin_states(self) -> Mapping[str, FSMState]:
        logger.debug("Getting plugin states")
        return {name: plugin.info.state
                for name, plugin in self._plugins.items()}

    def get_plugin_error(self):
        return {name: plugin.info.has_error
                for name, plugin in self._plugins.items()}
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

        self._plugins.update(plugins)

    def add_plugin_force(self, plugins: Mapping[str, PluginBase]) -> None:
        logger.debug("Adding plugins (skip duplicate): %s", plugins)
        new_plugins: Mapping[str, PluginBase] = {}

        for name, plugin in plugins.items():
            if self.__is_plugin_exist(name):
                logger.warning("Plugin %s already exists", name)
            else:
                new_plugins[name] = plugin

        self._plugins.update(new_plugins)
# endregion

# region method for all plugin
    def init_all_plugin(self) -> None:
        logger.debug("Initializing all plugins")
        for plugin in self._plugins.values():
            try:
                self.__change_state(FSMAction.INIT, plugin)
            except ValueError:
                ...
            except Exception as exc:
                logger.error(
                    "Failed to initialize plugin %s: %s",
                    plugin.info.name, exc
                )

    def start_all_plugin(self) ->  None:
        logger.debug("Starting all plugins")
        for plugin in self._plugins.values():
            try:
                self.__change_state(FSMAction.START, plugin)
            except ValueError:
                ...
            except Exception as exc:
                logger.error(
                    "Failed to started plugin %s: %s",
                    plugin.info.name, exc
                )

    def stop_all_plugin(self) -> None:
        logger.debug("Stopping all plugins")
        for plugin in self._plugins.values():
            try:
                self.__change_state(FSMAction.STOP, plugin)
            except ValueError:
                ...
            except Exception as exc:
                logger.error(
                    "Failed to stopped plugin %s: %s",
                    plugin.info.name, exc
                )
# endregion

# region method for solo plugin
    def initialize_plugin(self, plugin_name: str) -> None:
        logger.debug("Initializing plugin: '%s'", plugin_name)
        plugin = self.__get_plugin(plugin_name)
        if not plugin:
            raise PluginStateError("Failed to inviting plugin: '%s'",
                                   plugin_name)
        self.__change_state(FSMAction.INIT, plugin)

    def start_plugin(self, plugin_name: str) -> None:
        logger.debug("Starting plugin: %s", plugin_name)
        plugin = self.__get_plugin(plugin_name)
        if not plugin:
            raise PluginStateError("Failed to start plugin: '%s'",
                                   plugin_name)
        self.__change_state(FSMAction.START, plugin)

    def stop_plugin(self, plugin_name: str) -> None:
        logger.debug("Stopping plugin: %s", plugin_name)
        plugin = self.__get_plugin(plugin_name)
        if not plugin:
            raise PluginStateError("Failed to start plugin: '%s'",
                                   plugin_name)
        self.__change_state(FSMAction.STOP, plugin)


# endregion

    def __get_plugin(self, plugin_name) -> PluginBase | None:
        if not plugin_name or not isinstance(plugin_name, str):
            logger.error("Invalid plugin name: %s", plugin_name)
            return None
        return self._plugins.get(plugin_name)

    def __is_plugin_exist(self, plugin_name: str) -> bool:
        logger.debug("Checking if plugin exist: %s", plugin_name)
        return plugin_name in self._plugins

    def __change_state(self, action: FSMAction, plugin: PluginBase) -> None:
        self._state_transitions.perform_transition(plugin, action)
