from enum import IntEnum, auto


class FSMState(IntEnum):
    """Enum defining different states that the plugin can take."""
    CREATED = auto()
    INITIALIZED = auto()
    STARTED = auto()
    STOPPED = auto()
    FAILED = auto()
