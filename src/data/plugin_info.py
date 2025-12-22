from __future__ import annotations

from dataclasses import dataclass

from .plugin_state import PluginState

@dataclass(frozen=True)
class PluginInfo:
    """Basic information about plugin."""
    name: str
    state: PluginState = None
    description: str = None
    error: Exception = None
