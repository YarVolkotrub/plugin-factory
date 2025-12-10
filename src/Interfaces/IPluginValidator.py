from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .IPlugin import IPlugin


class IPluginValidator(ABC):
    @abstractmethod
    def is_valid(
        self, instance: 'IPlugin',
        plugins: dict[str, 'IPlugin']
    ) -> bool:
        ...
