from abc import ABC, abstractmethod
from pathlib import Path
from typing import Sequence


class StorageInterface(ABC):
    @property
    @abstractmethod
    def plugins(self) -> Sequence[Path]: ...
