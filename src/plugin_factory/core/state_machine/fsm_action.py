from __future__ import annotations

from enum import auto, IntEnum


class FSMAction(IntEnum):
    """Enum defining different actions that the plugin can take."""
    INIT = auto()
    START = auto()
    STOP = auto()
    FAIL = auto()
