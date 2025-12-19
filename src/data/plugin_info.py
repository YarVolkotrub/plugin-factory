from __future__ import annotations

from dataclasses import dataclass

from .plugin_state import PluginState

@dataclass(frozen=True)
class InfoBase:
    """Basic information about plugin."""
    name: str
    state: PluginState
    description: str | None = None
    error: str | None = None
