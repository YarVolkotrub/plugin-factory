from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class PluginAction:
    INITIALIZED: Final[str] = "init"
    STARTED: Final[str] = "start"
    STOPPED: Final[str] = "stop"
