from __future__ import annotations

from enum import auto, IntEnum


class PluginAction(IntEnum):
    """Enum defining different actions that the plugin can take."""
    INIT = auto()
    START = auto()
    STOP = auto()
    FAIL = auto()
    RESET = auto()
    RESTART = auto()
