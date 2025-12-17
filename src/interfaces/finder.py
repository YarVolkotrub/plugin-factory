from abc import ABC, abstractmethod
from pathlib import Path
from typing import Sequence


class PluginFinderBase(ABC):
    """
    Resolves filesystem paths to Python import paths.
    """

    @abstractmethod
    def find(self, files: Sequence[Path]) -> Sequence[str]:
        """
        Convert a plugin file path into an importable module path.

        Args:
            path: Filesystem path to plugin file.

        Returns:
            Fully-qualified import path.
        """
        raise NotImplementedError
