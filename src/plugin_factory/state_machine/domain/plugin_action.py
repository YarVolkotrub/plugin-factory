from __future__ import annotations

from enum import Enum, auto


class PluginAction(Enum):
    """Enum defining different actions that the plugin can take."""
    INIT = auto()
    START = auto()
    STOP = auto()
    FAIL = auto()
    RESET = auto()
    RESTART = auto()
