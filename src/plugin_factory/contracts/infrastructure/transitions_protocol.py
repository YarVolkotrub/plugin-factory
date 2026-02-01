from __future__ import annotations

from abc import abstractmethod
from typing import Mapping, TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from plugin_factory.core import FSMAction, FSMState


class TransitionProtocol(Protocol):
    @property
    @abstractmethod
    def allowed_transitions(self)  -> Mapping[
        FSMState,
        Mapping[FSMAction, FSMState]
    ]: ...
