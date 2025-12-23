from enum import Enum, auto


class PluginState(Enum):
    CREATED = auto()
    INITIALIZED = auto()
    STARTED = auto()
    STOPPED = auto()
    FAILED = auto()

    def is_active(self, state):
        ...
