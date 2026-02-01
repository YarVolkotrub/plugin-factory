from dataclasses import dataclass
from typing import Dict, ClassVar, Final
from types import MappingProxyType

from plugin_factory.core.plugins.plugin_method import PluginMethod
from plugin_factory.core.state_machine.fsm_action import FSMAction


@dataclass(frozen=True, slots=True)
class ActionMethodMap:
    __ACTION_METHOD_MAP: ClassVar[Dict[FSMAction, PluginMethod]] = {
        FSMAction.INIT: PluginMethod.INIT,
        FSMAction.START: PluginMethod.START,
        FSMAction.STOP: PluginMethod.STOP,
    }

    MAPPING: Final[MappingProxyType] = MappingProxyType(__ACTION_METHOD_MAP)

    def get_method_name(self, action: FSMAction) -> PluginMethod:
        return self.MAPPING.get(action)
