from __future__ import annotations

import logging
from types import MappingProxyType
from typing import TYPE_CHECKING, Dict

from plugin_factory.core import ACTION_TO_METHOD_MAP
from plugin_factory.exceptions import PluginStateError

if TYPE_CHECKING:
    from plugin_factory.core import (
        FSMAction,
        FSMState,
        PluginBase,
    )

logger = logging.getLogger(__name__)


class LifecycleTransitions:
    def __init__(self, state_transitions: MappingProxyType[
        FSMState,Dict[FSMAction, FSMState]
    ]):
        self.__allow_state_transitions = state_transitions

    def perform_transition(
            self,
            plugin: PluginBase,
            action: FSMAction
    ) -> None:
        current_state = plugin.info.state
        next_state = self.__get_next_state(current_state, action)

        try:
            self.__execute_plugin_action(plugin, action)
            plugin._apply_info(plugin.info.switch_state(next_state))
        except Exception as exc:
            plugin._apply_info(plugin.info.fail(exc))
            logger.exception(
                f"Plugin '{plugin.info.name}' "
                f"failed during action '{action.name}'",
            )

    def __get_next_state(self, current_state: FSMState,
                         action: FSMAction) -> FSMState:
        if not self.__is_action_allowed(current_state, action):
            raise PluginStateError(
                f"Action '{action.name}' "
                f"not allowed from state '{current_state.name}'"
            )

        return self.__allow_state_transitions[current_state][action]

    def __is_action_allowed(
            self,
            current_state: FSMState,
            action: FSMAction
    ) -> bool:
        return (current_state in self.__allow_state_transitions
                and action in self.__allow_state_transitions[current_state])

    def __execute_plugin_action(
            self,
            plugin: PluginBase,
            action: FSMAction
    ) -> None:
        method: object = self.__get_plugin_method(plugin, action)

        if method is None or not callable(method):
            return

        method()

    def __get_plugin_method(
            self,
            plugin: PluginBase,
            action: FSMAction
    ) -> object | None:
        try:
            method_name: str = ACTION_TO_METHOD_MAP[action]
            method: object = getattr(plugin, method_name, None)

            if method is None:
                raise PluginStateError(
                    f"Plugin missing lifecycle method: {action.name}")

        except KeyError:
            raise PluginStateError(
                f"No method mapped for action '{action.name}'")

        return method
