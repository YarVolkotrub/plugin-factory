from __future__ import annotations

from abc import abstractmethod
from typing import Mapping, TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from plugin_factory.core import PluginAction, PluginState


class TransitionProtocol(Protocol):
    @property
    @abstractmethod
    def allowed_transitions(self)  -> Mapping[
        PluginState,
        Mapping[PluginAction, PluginState]
    ]: ...
