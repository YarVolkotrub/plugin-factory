from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from plugin_factory.domain.plugin_base import PluginBase


class PluginValidatorInterface(Protocol):
    """
    Validates plugins against structural.
    """

    def is_valid(
        self, instance: PluginBase,
        plugins: dict[str, PluginBase]
    ) -> bool:
        ...
