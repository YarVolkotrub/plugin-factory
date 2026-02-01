from __future__ import annotations

from types import MappingProxyType
from typing import Final, Mapping, Dict

from plugin_factory.contracts import TransitionProtocol
from plugin_factory.core import FSMAction
from plugin_factory.core import FSMState


class FSMTransition(TransitionProtocol):
    """Enum defining transitions between states.

    STATE_DESCRIPTIONS:
        FSMState.CREATED - "Plugin created but not initialized",
        FSMState.INITIALIZED - "Plugin initialized and ready to start",
        FSMState.STARTED - "Plugin is running",
        FSMState.STOPPED - "Plugin stopped",
        FSMState.FAILED - "Plugin failed with error"

        ACTION_DESCRIPTIONS:
        FSMAction.INIT - "Initialize plugin",
        FSMAction.START - "Start plugin execution",
        FSMAction.STOP - "Stop plugin execution"
        FSMAction.FAIL - "Plugin failed with error",
    """


    def __init__(self):
        self.__allowed_transitions: Final[
            MappingProxyType[
                FSMState,
                Dict[FSMAction, FSMState]]
        ] = (MappingProxyType({
            FSMState.CREATED: {
                FSMAction.INIT: FSMState.INITIALIZED,
                FSMAction.FAIL: FSMState.FAILED,
            },
            FSMState.INITIALIZED: {
                FSMAction.START: FSMState.STARTED,
                FSMAction.FAIL: FSMState.FAILED,
            },
            FSMState.STARTED: {
                FSMAction.STOP: FSMState.STOPPED,
                FSMAction.FAIL: FSMState.FAILED,
            },
            FSMState.STOPPED: {
                FSMAction.INIT: FSMState.INITIALIZED,
                FSMAction.START: FSMState.STARTED,
                FSMAction.FAIL: FSMState.FAILED,
            },
            FSMState.FAILED: {
                FSMAction.INIT: FSMState.CREATED,
            },
        }))

    @property
    def allowed_transitions(self) -> Mapping[
        FSMState,
        Mapping[FSMAction, FSMState]
    ]:
        return self.__allowed_transitions
