from abc import ABC, abstractmethod
from pathlib import Path
from typing import Sequence


class PluginStorageBase(ABC):
    @abstractmethod
    def get_files(self) -> Sequence[Path]:
        """
        Filesystem-based plugin storage.

        Scans a directory recursively for plugin files
        matching the specified pattern.
        """
        raise NotImplementedError
