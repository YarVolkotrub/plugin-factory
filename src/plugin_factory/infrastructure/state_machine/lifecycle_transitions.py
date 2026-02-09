from __future__ import annotations

import logging
from types import MappingProxyType
from typing import TYPE_CHECKING, Dict

from plugin_factory.core import ACTION_METHOD_MAP
from plugin_factory.exceptions import PluginStateError

if TYPE_CHECKING:
    from plugin_factory.core import (
        FSMAction,
        FSMState,
        PluginBase,
        PluginMethod,
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

        if next_state not in self.__allow_state_transitions:
            raise PluginStateError(
                f"Transition not allowed: "
                f"state={current_state.name}, action={action.name}"
            )

        try:
            self.__execute_plugin_action(plugin, action)
            new_info = plugin.info.switch_state(next_state)
            plugin._apply_info(new_info)
        except Exception as exc:
            new_info = plugin.info.fail(exc)
            plugin._apply_info(new_info)

    def __get_next_state(
            self,
            current_state: FSMState,
            action: FSMAction
    ) -> FSMState | None:
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
        method = self.__get_plugin_method(plugin, action)

        if method is None or not callable(method):
            return

        method()

    def __get_plugin_method(
            self,
            plugin: PluginBase,
            action: FSMAction
    ) -> object | None:
        method_name: PluginMethod = ACTION_METHOD_MAP[action]

        return getattr(plugin, method_name, None)
