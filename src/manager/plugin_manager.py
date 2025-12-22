from __future__ import annotations
from typing import Mapping
import logging

from ..data.plugin_state import PluginState
from ..interfaces.plugin import PluginBase
from ..data.plugin_info import PluginInfo
from ..data.plugin_action import PluginAction

logger = logging.getLogger(__name__)


class PluginManager:
    ALLOWED_TRANSITIONS: dict[PluginState, set[str]] = {
        PluginState.CREATED: {PluginAction.INIT},
        PluginState.INITIALIZED: {PluginAction.START},
        PluginState.STARTED: {PluginAction.STOP},
        PluginState.STOPPED: {PluginAction.INIT, PluginAction.START},
        PluginState.FAILED: set(),
    }

    def __init__(self, plugins: Mapping[str, PluginBase]) -> None:
        if not plugins:
            raise ValueError("plugins mapping must not be empty")

        self.__plugins: Mapping[str, PluginBase] = plugins
        self.__states: dict[str, PluginState] = {
            name: PluginState.CREATED for name in plugins
        }
        self.__errors: dict[str, Exception | None] = {
            name: None for name in plugins
        }
        logger.debug(f"init {__class__.__name__}")


    def init_all(self) -> None:
        logger.debug("init all called")

        for plugin_name in self.__plugins.keys():
            self.__execute(plugin_name, PluginAction.INIT, PluginState.INITIALIZED)

    def start(self, plugin_name: str) -> None:
        logger.debug("start called")

        self.__execute(plugin_name, PluginAction.START, PluginState.STARTED)

    def stop(self, plugin_name: str) -> None:
        logger.debug("stop called")

        self.__execute(plugin_name, PluginAction.STOP, PluginState.STOPPED)

    def start_all(self) ->  None:
        logger.debug("start all called")

        for plugin_name in self.__plugins:
            self.__execute(plugin_name, PluginAction.START, PluginState.STARTED)

    def stop_all(self) -> None:
        logger.debug("stop all called")

        for plugin_name in self.__plugins:
            self.__execute(plugin_name, PluginAction.STOP, PluginState.STOPPED)

    def get_info(self) -> dict[str, PluginInfo | None]:
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

    def get_states(self) -> dict[str, PluginState]:
        return dict(self.__states)

    def __execute(
            self,
            plugin_name: str,
            action_name: str,
            success_state: PluginState,
    ) -> None:
        logger.info(f"Plugin '{plugin_name}' - {action_name}")

        self.__check_transition(plugin_name, action_name)
        plugin = self.__get_plugin(plugin_name)
        method = getattr(plugin, action_name, None)

        if method is None:
            raise AttributeError(
                f"Plugin '{plugin_name}' has no method '{action_name}'"
            )

        try:
            getattr(plugin, action_name)()
            self.__states[plugin_name] = success_state
            logger.debug(f"Plugin '{plugin_name}' - {action_name} - success")
        except Exception as exc:
            self.__states[plugin_name] = PluginState.FAILED
            self.__errors[plugin_name] = exc
            logger.debug(f"Plugin '{plugin_name}' - {action_name} - failed")
            raise

    def __get_plugin(self, plugin_name: str) -> PluginBase:
        if not isinstance(plugin_name, str) or not plugin_name.strip():
            raise ValueError("plugin_name must be a non-empty string")

        try:
            return self.__plugins[plugin_name]
        except KeyError:
            raise KeyError(f"Plugin not found: {plugin_name}") from None

    def __check_transition(
            self,
            plugin_name: str,
            action: str,
    ) -> None:
        state = self.__states[plugin_name]

        allowed = self.ALLOWED_TRANSITIONS.get(state, set())

        if action not in allowed:
            raise InvalidPluginTransition(
                f"Plugin '{plugin_name}': "
                f"action '{action}' not allowed in state {state.name}"
            )

class InvalidPluginTransition(RuntimeError):
    pass