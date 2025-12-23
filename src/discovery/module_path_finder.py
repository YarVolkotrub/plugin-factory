from pathlib import Path
from typing import Sequence
import logging

from src.interfaces.finder import PluginFinderBase

logger = logging.getLogger(__name__)


class ModulePathFinder(PluginFinderBase):
    def __init__(self, root_package: str = "plugins") -> None:
        logger.debug(f"init {__class__.__name__}")

        self._root_package = root_package

    def get(self, files: Sequence[Path]) -> Sequence[str]:
        if not files:
            return []

        module_names: list[str] = []

        for file in files:
            module = file.with_suffix("")
            parts = module.parts

            try:
                idx = parts.index(self._root_package)
            except ValueError:
                continue

            import_path = ".".join(parts[idx:])
            module_names.append(import_path)

        return module_names
