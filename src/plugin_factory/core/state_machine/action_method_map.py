from dataclasses import dataclass
from typing import Dict, ClassVar
from plugin_factory.core.state_machine.plugin_action import PluginAction
from plugin_factory.core.plugins.plugin_method import PluginMethod


@dataclass(frozen=True, slots=True)
class ActionMethodMap:
    ACTION_METHOD_MAP: ClassVar[Dict[PluginAction, PluginMethod]] = {
        PluginAction.INIT: PluginMethod.INIT,
        PluginAction.START: PluginMethod.START,
        PluginAction.STOP: PluginMethod.STOP,
        PluginAction.FAIL: PluginMethod.FAIL,
        PluginAction.RESET: PluginMethod.RESET,
        PluginAction.RESTART: PluginMethod.RESTART,
    }

    def get_method_name(self, action: PluginAction) -> PluginMethod:
        return self.ACTION_METHOD_MAP.get(action)
