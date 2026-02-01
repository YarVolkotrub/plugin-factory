from enum import StrEnum


class PluginMethod(StrEnum):
    INIT = "initialize"
    START = "start",
    STOP = "shutdown"
