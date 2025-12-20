from typing import Sequence, Protocol
from pathlib import Path


class PluginFinderBase(Protocol):
    """
    Resolves filesystem paths to Python import paths.
    """

    def find(self, module: Sequence[Path]) -> Sequence[str]:
        """
        Convert a plugin file path into an importable module path.

        Args:
            path: Filesystem path to plugin file.

        Returns:
            Fully-qualified import path.
            :param module:
        """
        raise NotImplementedError
