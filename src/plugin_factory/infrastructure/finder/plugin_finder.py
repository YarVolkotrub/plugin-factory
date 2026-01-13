from __future__ import annotations

import logging
from pathlib import Path
from typing import Sequence, List

from plugin_factory.contracts import StorageProtocol
from plugin_factory.contracts import FinderPathProtocol
from plugin_factory.exceptions.exceptions import PluginStorageError

logger = logging.getLogger(__name__)


class PluginFinderProtocol(StorageProtocol, FinderPathProtocol):
    def __init__(self) -> None:
        self._plugins: List[Path] = []

    @property
    def plugins(self) -> Sequence[Path]:
        return self._plugins

    def find_in_directory(
            self,
            plugin_dir: Path,
            pattern: str
    ) -> None:
        logger.debug("Scanning for plugin files in '%s' with pattern '%s'",
                    plugin_dir, pattern)

        self.__validate_directory(plugin_dir)

        files: List[Path] = list(plugin_dir.rglob(pattern))
        logger.info("Found %d plugin files in '%s'", len(files),
                    plugin_dir)

        for file in files:
            if file.is_file():
                self.__add_file(file)

    def find_in_directories(self, directories: List[Path], pattern: str):
        for directory in directories:
            self.find_in_directory(directory, pattern)

    def __add_file(self, file: Path) -> None:
        if file in self._plugins:
            logger.debug("Found plugin file: %s", file)
            return
        self._plugins.append(file)
        logger.debug("Adding plugin file: '%s'", file)

    def __validate_directory(self, directory: Path) -> None:
        if not directory.exists():
            error_msg = f"Plugins directory does not exist: {directory}"
            logger.error("Directory not found: '%s'", directory)
            raise PluginStorageError(error_msg)

        if not directory.is_dir():
            error_msg = f"Plugin path is not a directory: {directory}"
            logger.error("Path is not a directory: '%s'", directory)
            raise PluginStorageError(error_msg)
