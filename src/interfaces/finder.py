from typing import Sequence, Protocol
from pathlib import Path


class PluginFinderBase(Protocol):
    """
    Resolves filesystem paths to Python import paths.
    """

    def get(self, files: Sequence[Path]) -> Sequence[str]:
        """
        Convert a plugin file path into an importable module path.
        """
