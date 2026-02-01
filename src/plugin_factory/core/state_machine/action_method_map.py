from types import MappingProxyType
from typing import Final

from plugin_factory.core.plugins.plugin_method import PluginMethod
from plugin_factory.core.state_machine.fsm_action import FSMAction

ACTION_METHOD_MAP: Final[MappingProxyType[
    FSMAction, PluginMethod]
] = MappingProxyType({
    FSMAction.INIT: PluginMethod.INIT,
    FSMAction.START: PluginMethod.START,
    FSMAction.STOP: PluginMethod.STOP,
})
