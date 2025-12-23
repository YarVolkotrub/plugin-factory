from pathlib import Path
from typing import Sequence
import logging

from ..interfaces.finder import PluginFinderBase

logger = logging.getLogger(__name__)


class ModulePathFinder(PluginFinderBase):
    def __init__(self, root_package: str = "plugins") -> None:
        self._root_package = root_package

        logger.debug("Initialized %s with root package: '%s'",
                    self.__class__.__name__, root_package)

    def get(self, files: Sequence[Path]) -> Sequence[str]:
        logger.debug("Converting %d file(s) to module import paths", len(files))

        if not files:
            logger.debug("No files to process")
            return []

        module_names: list[str] = []

        for file in files:
            logger.debug("Processing file: %s", file)

            module = file.with_suffix("")
            parts = module.parts

            try:
                idx = parts.index(self._root_package)
            except ValueError:
                logger.debug("Skipping file '%s': root package '%s' not found in path",
                            file.name, self._root_package)
                continue

            import_path = ".".join(parts[idx:])
            module_names.append(import_path)
            logger.debug("Converted to import path: %s", import_path)

        return module_names
