from __future__ import annotations
from functools import lru_cache
from typing import Mapping, ClassVar, Optional
from types import MappingProxyType
import logging

from ..domain.plugin_state import PluginState
from ..domain.plugin import PluginBase
from ..domain.plugin_info import PluginInfo
from ..domain.plugin_action import PluginAction
from ..domain.plugin_constants import PluginConstants

logger = logging.getLogger(__name__)


class PluginStateManager:
    _ALLOWED_TRANSITIONS: ClassVar[
        Mapping[
            PluginState,
            frozenset[PluginAction]
        ]
    ] = PluginConstants.ALLOWED_TRANSITIONS

    def __init__(self, plugins: Mapping[str, PluginBase]) -> None:
        logger.debug(f"init {__class__.__name__}")

        if not plugins:
            raise ValueError("plugins mapping must not be empty")

        self.__plugins: Mapping[str, PluginBase] = plugins
        self.__states: dict[str, PluginState] = {}
        self.__errors: dict[str, Optional[Exception] | None] = {}

        for name, plugin in plugins.items():
            self.__states[name] = plugin.info.state
            self.__errors[name] = plugin.info.error

        self.__plugin_names: tuple[str, ...] = tuple(self.__plugins.keys())

        logger.debug("Initialized %s with %d plugins",
                    self.__class__.__name__, len(plugins))

    @staticmethod
    @lru_cache(maxsize=6)
    def __get_allowed_actions(state: PluginState) -> frozenset[PluginAction]:
        return PluginStateManager._ALLOWED_TRANSITIONS.get(state, frozenset())

    def init_all_plugin(self) -> None:
        logger.debug("Initializing all plugins")

        for plugin_name in self.__plugin_names:
            self.__perform_transition(plugin_name, PluginAction.INIT, PluginState.INITIALIZED)

    def start_plugin(self, plugin_name: str) -> None:
        logger.debug("Starting plugin: %s", plugin_name)

        self.__perform_transition(plugin_name, PluginAction.START, PluginState.STARTED)

    def stop_plugin(self, plugin_name: str) -> None:
        logger.debug("Stopping plugin: %s", plugin_name)

        self.__perform_transition(plugin_name, PluginAction.STOP, PluginState.STOPPED)

    def start_all_plugin(self) ->  None:
        logger.debug("Starting all plugins")

        for plugin_name in self.__plugin_names:
            self.__perform_transition(plugin_name, PluginAction.START, PluginState.STARTED)

    def stop_all_plugin(self) -> None:
        logger.debug("Stopping all plugins")

        for plugin_name in self.__plugin_names:
            self.__perform_transition(plugin_name, PluginAction.STOP, PluginState.STOPPED)

    def get_plugin_info(self) -> dict[str, PluginInfo | None]:
        logger.debug("Getting plugin info")

        result: dict[str, PluginInfo | None] = {}

        for name, plugin in self.__plugins.items():
            try:
                result[name] = PluginInfo(
                    name=name,
                    state=self.__states[name],
                    error=self.__errors[name],
                )
            except Exception as exc:
                logger.warning("Failed to get info for plugin '%s': %s", name,
                               exc)
                result[name] = PluginInfo(
                    name=name,
                    state=self.__states[name],
                    error=exc,
                )
        return result

    def get_plugin_states(self) -> MappingProxyType[str, PluginState]:
        logger.debug("Getting plugin states")
        return MappingProxyType(self.__states)

    def __perform_transition(
            self,
            plugin_name: str,
            action: str,
            target_state: PluginState,
    ) -> None:
        logger.info("Transitioning plugin '%s': %s -> %s",
                   plugin_name, action, target_state.value)

        if self.__is_transition_allowed(plugin_name, action):
            logger.error("Transition not allowed for plugin '%s': %s",
                        plugin_name, action)
            return

        plugin = self.__get_plugin(plugin_name)
        method = getattr(plugin, action, None)

        if method is None:
            raise AttributeError(
                f"Plugin '{plugin_name}' has no method '{action}'"
            )

        try:
            getattr(plugin, action)()
            self.__states[plugin_name] = target_state
            logger.debug("Plugin '%s' transition successful: %s -> %s",
                        plugin_name, action, target_state.value)
        except Exception as exc:
            self.__states[plugin_name] = PluginState.FAILED
            self.__errors[plugin_name] = exc
            logger.error("Plugin '%s' transition failed: %s - %s",
                        plugin_name, action, exc)
            raise

    def __get_plugin(self, plugin_name: str) -> PluginBase:
        if not isinstance(plugin_name, str) or not plugin_name.strip():
            raise ValueError("plugin_name must be a non-empty string")

        try:
            return self.__plugins[plugin_name]
        except KeyError:
            logger.error("Plugin not found: %s", plugin_name)
            raise KeyError(f"Plugin not found: {plugin_name}") from None

    def __is_transition_allowed(
            self,
            plugin_name: str,
            action: str,
    ) -> bool:
        current_state = self.__states[plugin_name]
        allowed = action not in self.__get_allowed_actions(current_state)

        if allowed:
            logger.debug("Transition allowed for '%s': %s (current state: %s)",
                         plugin_name, action, current_state.value)
        else:
            logger.debug("Transition denied for '%s': %s (current state: %s)",
                         plugin_name, action, current_state.value)

        return allowed
