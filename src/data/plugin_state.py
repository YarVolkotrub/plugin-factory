from enum import Enum, auto


class PluginState(Enum):
    CREATED = auto()   # объект создан
    INITIALIZED = auto()
    STARTED = auto()
    STOPPED = auto()
    FAILED = auto()
