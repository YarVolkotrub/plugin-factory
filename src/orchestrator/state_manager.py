from __future__ import annotations

from functools import lru_cache
from typing import Mapping, ClassVar
import logging

from src.domain.plugin_state import PluginState
from src.domain.plugin import PluginBase
from src.domain.plugin_info import PluginInfo
from src.domain.plugin_action import PluginAction
from src.domain.plugin_constants import PluginConstants

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
        self.__errors: dict[str, Exception | None] = {}

        self.__states = {name: PluginState.CREATED for name in plugins}
        self.__errors = {name: None for name in plugins}

        self.__plugin_names: tuple[str, ...] = tuple(self.__plugins.keys())

    @staticmethod
    @lru_cache(maxsize=6)
    def __get_allowed_actions(state: PluginState) -> frozenset[PluginAction]:
        return PluginStateManager._ALLOWED_TRANSITIONS.get(state, frozenset())

    def init_all_plugin(self) -> None:
        logger.debug("init all called")

        for plugin_name in self.__plugin_names:
            self.__perform_transition(plugin_name, PluginAction.INIT, PluginState.INITIALIZED)

    def start_plugin(self, plugin_name: str) -> None:
        logger.debug("start called")

        self.__perform_transition(plugin_name, PluginAction.START, PluginState.STARTED)

    def stop_plugin(self, plugin_name: str) -> None:
        logger.debug("stop called")

        self.__perform_transition(plugin_name, PluginAction.STOP, PluginState.STOPPED)

    def start_all_plugin(self) ->  None:
        logger.debug("start all called")

        for plugin_name in self.__plugin_names:
            self.__perform_transition(plugin_name, PluginAction.START, PluginState.STARTED)

    def stop_all_plugin(self) -> None:
        logger.debug("stop all called")

        for plugin_name in self.__plugin_names:
            self.__perform_transition(plugin_name, PluginAction.STOP, PluginState.STOPPED)

    def get_plugin_info(self) -> dict[str, PluginInfo | None]:
        logger.debug("get info called")

        result: dict[str, PluginInfo | None] = {}

        for name, plugin in self.__plugins.items():
            try:
                result[name] = PluginInfo(
                    name=name,
                    state=self.__states[name],
                    error=self.__errors[name],
                )
            except Exception as exc:
                result[name] = PluginInfo(
                    name=name,
                    state=self.__states[name],
                    error=exc,
                )

        return result

    def get_plugin_states(self) -> dict[str, PluginState]:
        return dict(self.__states)

    def __perform_transition(
            self,
            plugin_name: str,
            action: str,
            target_state: PluginState,
    ) -> None:
        logger.info(f"Plugin '{plugin_name}' - {action}")

        if self.__is_transition_allowed(plugin_name, action):
            logger.error(f"Plugin '{plugin_name}' - {action} - failed")
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
            logger.debug(f"Plugin '{plugin_name}' - {action} - success")
        except Exception as exc:
            self.__states[plugin_name] = PluginState.FAILED
            self.__errors[plugin_name] = exc
            logger.debug(f"Plugin '{plugin_name}' - {action} - failed")
            raise

    def __get_plugin(self, plugin_name: str) -> PluginBase:
        if not isinstance(plugin_name, str) or not plugin_name.strip():
            raise ValueError("plugin_name must be a non-empty string")

        try:
            return self.__plugins[plugin_name]
        except KeyError:
            raise KeyError(f"Plugin not found: {plugin_name}") from None

    def __is_transition_allowed(
            self,
            plugin_name: str,
            action: str,
    ) -> bool:
        current_state = self.__states[plugin_name]

        return action not in self.__get_allowed_actions(current_state)
