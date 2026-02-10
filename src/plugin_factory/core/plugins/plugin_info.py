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
    error: Optional[BaseException] = field(
        default=None, compare=False, repr=False)

    def __post_init__(self):
        if not isinstance(self.state, FSMState):
            raise TypeError("state must be FSMState")

        if self.error is not None and not isinstance(self.error, Exception):
            raise TypeError("error must be Exception or None")

        if not self.name:
            raise ConfigurationError("Plugin name is empty")

        if self.state is FSMState.FAILED and self.error is None:
            raise RuntimeError("FAILED state requires error")

        if self.state is not FSMState.FAILED and self.error is not None:
            raise RuntimeError("error allowed only in FAILED state")

    @property
    def has_error(self) -> bool:
        """Check if plugin has error."""
        return self.error is not None or self.state is FSMState.FAILED

    def switch_state(self, new_state: FSMState):
        """Switch the state of the plugin."""
        if not isinstance(new_state, FSMState):
            raise TypeError("new_state must be FSMState")

        if new_state is FSMState.FAILED:
            raise ValueError("Use fail()")

        new_info: PluginInfo = replace(self, state=new_state)

        assert new_info is not self
        assert new_info.state is new_state

        return new_info

    def fail(self, error: BaseException) -> PluginInfo:
        """Set the error of the plugin."""
        if not isinstance(error, Exception):
            raise TypeError("error must be Exception")

        new_info: PluginInfo = replace(self, state=FSMState.FAILED, error=error)

        assert new_info is not self
        assert new_info.error is error

        return new_info
