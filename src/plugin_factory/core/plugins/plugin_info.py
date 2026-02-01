from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Optional

from plugin_factory.core.state_machine.fsm_state import FSMState
from plugin_factory.exceptions import ConfigurationError


@dataclass(frozen=True, slots=True)
class PluginInfo:
    """Basic information about plugin.
    PluginInfo is created only during plugin instantiation
    and must not be created manually elsewhere.
    """
    name: str
    state: FSMState = field(default=FSMState.CREATED)
    description: Optional[str] = field(default=None, compare=False)
    error: Optional[BaseException] = field(default=None, compare=False, repr=False)

    def __post_init__(self):
        if not self.name:
            raise ConfigurationError("Plugin name is empty")

    @property
    def has_error(self) -> bool:
        """Check if plugin has error."""
        return self.error is not None or self.state is FSMState.FAILED

    def switch_state(self, new_state: FSMState):
        """Switch the state of the plugin."""
        if new_state is FSMState.FAILED:
            raise ValueError("Use fail()")

        return replace(self, state=new_state)

    def fail(self, exc: BaseException) -> PluginInfo:
        """Set the error of the plugin."""
        return replace(self, state=FSMState.FAILED, error=exc)
