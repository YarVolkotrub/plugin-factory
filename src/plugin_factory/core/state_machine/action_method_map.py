from typing import Dict, Final

from plugin_factory.core.plugins.plugin_method import PluginMethod
from plugin_factory.core.state_machine.fsm_action import FSMAction

ACTION_METHOD_MAP: Final[Dict[FSMAction, PluginMethod]] = {
    FSMAction.INIT: PluginMethod.INIT,
    FSMAction.START: PluginMethod.START,
    FSMAction.STOP: PluginMethod.STOP
}

def get_method_name(action: FSMAction) -> PluginMethod:
    return ACTION_METHOD_MAP[action]
