from __future__ import annotations

from typing import TYPE_CHECKING

from plugin_factory.core import ActionMethodMap, PluginAction

if TYPE_CHECKING:
    from plugin_factory.contracts import TransitionProtocol
    from plugin_factory.core import (
        PluginState,
        PluginBase,
        PluginMethod,
    )


class LifecycleTransitions:
    def __init__(self, state_transitions: TransitionProtocol,
                 ):
        self.__allow_state_transitions = state_transitions.allowed_transitions
        self.__method_map = ActionMethodMap()

    def perform_transition(
            self,
            plugin: PluginBase,
            action: PluginAction
    ) -> None:
        current_state = plugin.info.state
        next_state = self.__get_next_state(current_state, action)

        if next_state not in self.__allow_state_transitions:
            return

        self.__execute_plugin_action(plugin, action)
        plugin.set_state(next_state)

    def __get_next_state(
            self,
            current_state: PluginState,
            action: PluginAction
    ) -> PluginState | None:
        if not self.__is_action_allowed(current_state, action):
            return None
        return self.__allow_state_transitions[current_state][action]

    def __is_action_allowed(
            self,
            current_state: PluginState,
            action: PluginAction
    ) -> bool:
        return (current_state in self.__allow_state_transitions
                and action in self.__allow_state_transitions[current_state])

    def __execute_plugin_action(
            self,
            plugin: PluginBase,
            action: PluginAction
    ) -> None:
        method = self.__get_plugin_method(plugin, action)

        if method is None or not callable(method):
            return

        method()

    def __get_plugin_method(
            self,
            plugin: PluginBase,
            action: PluginAction
    ) -> object | None:
        method_name: PluginMethod = self.__method_map.get_method_name(action)

        return getattr(plugin, method_name, None)
