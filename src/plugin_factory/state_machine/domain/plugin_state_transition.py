from __future__ import annotations

from typing import Final, Mapping, Dict
from types import MappingProxyType

from plugin_factory.state_machine.domain import PluginAction
from plugin_factory.state_machine.domain import PluginState
from plugin_factory.state_machine.interface import TransitionInterface


class PluginStateTransitions(TransitionInterface):
    """Enum defining transitions between states.

    STATE_DESCRIPTIONS:
        PluginState.CREATED - "Plugin created but not initialized",
        PluginState.INITIALIZED - "Plugin initialized and ready to start",
        PluginState.STARTED - "Plugin is running",
        PluginState.STOPPED - "Plugin stopped",
        PluginState.FAILED - "Plugin failed with error"

        ACTION_DESCRIPTIONS:
        PluginAction.INIT - "Initialize plugin",
        PluginAction.START - "Start plugin execution",
        PluginAction.STOP - "Stop plugin execution"
        PluginAction.FAIL - "Plugin failed with error",
        PluginAction.RESET - "Reset plugin state",
        PluginAction.RESTART - "Restart plugin execution",
    """


    def __init__(self):
        self.__allowed_transitions: Final[
            MappingProxyType[
                PluginState,
                Dict[PluginAction, PluginState]]
        ] = (MappingProxyType({
            PluginState.CREATED: {
                PluginAction.INIT: PluginState.INITIALIZED,
                PluginAction.FAIL: PluginState.FAILED,
            },
            PluginState.INITIALIZED: {
                PluginAction.START: PluginState.STARTED,
                PluginAction.FAIL: PluginState.FAILED,
                PluginAction.RESET: PluginState.CREATED,
            },
            PluginState.STARTED: {
                PluginAction.STOP: PluginState.STOPPED,
                PluginAction.FAIL: PluginState.FAILED,
            },
            PluginState.STOPPED: {
                PluginAction.INIT: PluginState.INITIALIZED,
                PluginAction.START: PluginState.STARTED,
                PluginAction.RESET: PluginState.CREATED,
                PluginAction.FAIL: PluginState.FAILED,
            },
            PluginState.FAILED: {
                PluginAction.RESET: PluginState.CREATED,
                PluginAction.RESTART: PluginState.INITIALIZED,
            },
        }))

    @property
    def allowed_transitions(self) -> Mapping[PluginState, Mapping[PluginAction, PluginState]]:
        return self.__allowed_transitions
