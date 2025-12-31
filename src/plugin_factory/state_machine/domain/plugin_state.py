from enum import Enum, auto


class PluginState(Enum):
    """Enum defining different states that the plugin can take."""
    CREATED = auto()
    INITIALIZED = auto()
    STARTED = auto()
    STOPPED = auto()
    FAILED = auto()

