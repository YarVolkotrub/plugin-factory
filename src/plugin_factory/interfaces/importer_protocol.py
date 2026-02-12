from abc import abstractmethod
from pathlib import Path
from types import ModuleType
from typing import Protocol


class ImporterProtocol(Protocol):
    @abstractmethod
    def import_module(self, plugin: Path) -> ModuleType: ...
