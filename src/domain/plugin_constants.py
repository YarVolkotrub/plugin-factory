from __future__ import annotations
from typing import Final
from types import MappingProxyType

from src.domain.plugin_action import PluginAction
from src.domain.plugin_state import PluginState


class PluginConstants:
    ALLOWED_TRANSITIONS: Final = MappingProxyType({
        PluginState.CREATED: frozenset([PluginAction.INIT]),
        PluginState.INITIALIZED: frozenset([PluginAction.START]),
        PluginState.STARTED: frozenset([PluginAction.STOP]),
        PluginState.STOPPED: frozenset([PluginAction.INIT, PluginAction.START]),
        PluginState.FAILED: frozenset(),
    })

    STATE_DESCRIPTIONS: Final = MappingProxyType({
        PluginState.CREATED: "Plugin created but not initialized",
        PluginState.INITIALIZED: "Plugin initialized and ready to start",
        PluginState.STARTED: "Plugin is running",
        PluginState.STOPPED: "Plugin stopped",
        PluginState.FAILED: "Plugin failed with error",
    })

    ACTION_DESCRIPTIONS: Final = MappingProxyType({
        PluginAction.INIT: "Initialize plugin",
        PluginAction.START: "Start plugin execution",
        PluginAction.STOP: "Stop plugin execution",
    })
