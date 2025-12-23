from __future__ import annotations
from typing import Optional
from dataclasses import dataclass, field

from .plugin_state import PluginState

@dataclass(frozen=True, slots=True)
class PluginInfo:
    """Basic information about plugin."""
    name: str
    state: PluginState = field(default=PluginState.CREATED)
    description: Optional[str] = field(default=None, compare=False)
    error: Optional[Exception] = field(default=None, compare=False, repr=False)

    @property
    def is_active(self) -> bool:
        """Check if plugin is active (cached property)."""
        return PluginState.is_active(self.state)

    @property
    def has_error(self) -> bool:
        """Check if plugin has error."""
        return self.error is not None
