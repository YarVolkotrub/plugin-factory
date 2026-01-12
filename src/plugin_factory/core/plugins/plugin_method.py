from enum import StrEnum


class PluginMethod(StrEnum):
    INIT = "initialize"
    START = "start",
    STOP = "shutdown"
    FAIL = "fail"
    RESET = "reset"
    RESTART = "restart"