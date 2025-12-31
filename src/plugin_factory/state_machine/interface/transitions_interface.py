from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Mapping, TYPE_CHECKING

if TYPE_CHECKING:
    from plugin_factory.state_machine.domain.plugin_state import PluginState
    from plugin_factory.state_machine.domain.plugin_action import PluginAction


class TransitionInterface(ABC):
    @property
    @abstractmethod
    def allowed_transitions(self)  -> Mapping[
        PluginState,
        Mapping[PluginAction, PluginState]]: ...
