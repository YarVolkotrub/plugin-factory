from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class PluginAction:
    INIT = "init"
    START = "start"
    STOP = "stop"
