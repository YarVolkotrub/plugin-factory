from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class PluginAction:
    INIT = "init"
    START = "start"
    STOP = "stop"

    @property
    def required(self) -> bool:
        return self in {
            PluginAction.INIT,
            PluginAction.START,
            PluginAction.STOP,
        }
