from __future__ import annotations

from typing import Optional
from dataclasses import dataclass, field, replace

from plugin_factory.state_machine.domain.plugin_state import PluginState


@dataclass(frozen=True, slots=True)
class PluginInfo:
    """Basic information about plugin."""
    name: str
    state: PluginState = field(default=PluginState.CREATED)
    description: Optional[str] = field(default=None, compare=False)
    error: Optional[Exception] = field(default=None, compare=False, repr=False)

    @property
    def has_error(self) -> bool:
        """Check if plugin has error."""
        return self.error is not None

    def switch_state(self, state: PluginState):
        """Switch the state of the plugin."""
        return replace(self, state=state)

    def set_error(self, error: Exception):
        """Set the error of the plugin."""
        return replace(self, error=error)
