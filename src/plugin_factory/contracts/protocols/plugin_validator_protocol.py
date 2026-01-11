from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from plugin_factory.core import PluginBase


class PluginValidatorProtocol(Protocol):
    @abstractmethod
    def is_valid(
        self, instance: PluginBase,
        plugins: dict[str, PluginBase]
    ) -> bool: ...
