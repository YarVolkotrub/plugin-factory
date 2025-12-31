from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .interface.transitions_interface import TransitionInterface
    from plugin_factory.state_machine.domain.plugin_action import PluginAction


class StateTransition:
    """for the future"""
    def __init__(self, state_transitions: TransitionInterface,
                 ):
        self.__allow_state_transitions = state_transitions.allowed_transitions

    def is_action_allowed(self, action: PluginAction) -> bool:
        return action in self.__allow_state_transitions





