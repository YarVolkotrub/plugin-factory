from pathlib import Path
from typing import Sequence
import logging

from ..interfaces.finder import PluginFinderBase

logger = logging.getLogger(__name__)


class LocalPluginFinder(PluginFinderBase):
    def __init__(self, root_package: str = "plugins") -> None:
        self._root_package = root_package
        logger.debug(f"init {__class__.__name__}")

    def find(self, files: Sequence[Path]) -> Sequence[str]:
        result: list[str] = []

        for file in files:
            module = file.with_suffix("")
            parts = module.parts

            try:
                idx = parts.index(self._root_package)
            except ValueError:
                continue

            import_path = ".".join(parts[idx:])
            result.append(import_path)

        return result
