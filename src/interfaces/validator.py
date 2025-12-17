from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .plugin import PluginBase


class PluginValidatorBase(ABC):
    """
    Validates plugins against structural.
    """

    @abstractmethod
    def is_valid(
        self, instance: 'PluginBase',
        plugins: dict[str, 'PluginBase']
    ) -> bool:
        ...
