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


class LifecycleManager:
    def __init__(self, allow_state: MappingProxyType[
        FSMState,Dict[FSMAction, FSMState]
    ]) -> None:
        self._plugins: Dict[str, PluginBase] = {}
        self._state_transitions = LifecycleTransitions(allow_state)

# region Plugin Information Methods
    def get_plugin_info(self) -> Mapping[str, PluginInfo]:
        return {name: plugin.info
                for name, plugin in self._plugins.items()}

    def get_plugin_states(self) -> Mapping[str, FSMState]:
        return {name: plugin.info.state
                for name, plugin in self._plugins.items()}

    def get_plugin_has_error(self):
        return {name: plugin.info.has_error
                for name, plugin in self._plugins.items()}

    def get_plugins_error(self):
        return {name: plugin.info.error
                for name, plugin in self._plugins.items()
                if plugin.info.has_error}
# endregion

# region method add plugin
    def add_plugins(self, plugins: Mapping[str, PluginBase]) -> None:
        for name in plugins:
            if name in self._plugins:
                raise PluginStateError(f"Plugin '$s' already exists" % name)

        self._plugins.update(plugins)

    def add_plugin_force(self, plugins: Mapping[str, PluginBase]) -> None:
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
        for plugin in self._plugins.values():
            self.__change_state(FSMAction.INIT, plugin)

    def start_all_plugin(self) ->  None:
        for plugin in self._plugins.values():
            self.__change_state(FSMAction.START, plugin)

    def stop_all_plugin(self) -> None:
        for plugin in self._plugins.values():
            self.__change_state(FSMAction.STOP, plugin)

# endregion

# region method for solo plugin
    def initialize_plugin(self, plugin_name: str) -> None:
        plugin = self.__require_plugin(plugin_name)
        self.__change_state(FSMAction.INIT, plugin)

    def start_plugin(self, plugin_name: str) -> None:
        plugin = self.__require_plugin(plugin_name)
        self.__change_state(FSMAction.START, plugin)

    def stop_plugin(self, plugin_name: str) -> None:
        plugin = self.__require_plugin(plugin_name)
        self.__change_state(FSMAction.STOP, plugin)

# endregion
    def __require_plugin(self, plugin_name) -> PluginBase:
        if not plugin_name or not isinstance(plugin_name, str):
            raise PluginStateError("Invalid plugin name: %s" % plugin_name)

        try:
            return self._plugins[plugin_name]
        except KeyError:
            raise PluginStateError("Plugin '%s' not found" % plugin_name)

    def __is_plugin_exist(self, plugin_name: str) -> bool:
        return plugin_name in self._plugins

    def __change_state(self, action: FSMAction, plugin: PluginBase) -> None:
        self._state_transitions.perform_transition(plugin, action)
        logger.info(
            "FSM transition plugin=%s action=%s state=%s",
            plugin.info.name,
            action.name,
            plugin.info.state.name,
        )
