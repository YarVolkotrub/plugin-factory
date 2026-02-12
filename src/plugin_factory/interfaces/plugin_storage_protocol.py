from abc import abstractmethod
from pathlib import Path
from typing import Sequence, Protocol


class PluginStorageProtocol(Protocol):
    @property
    @abstractmethod
    def plugins(self) -> Sequence[Path]: ...
