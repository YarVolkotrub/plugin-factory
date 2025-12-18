from enum import Enum, auto


class PluginState(Enum):
    INIT = auto()
    STARTED = auto()
    STOPPED = auto()
    FAILED = auto()
