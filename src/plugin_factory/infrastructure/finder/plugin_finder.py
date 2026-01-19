from __future__ import annotations

import logging
from pathlib import Path
from typing import Sequence, List

from plugin_factory.contracts import FinderManagerProtocol
from plugin_factory.contracts import StorageProtocol
from plugin_factory.core.finder.finder_storage import FinderStorage
from plugin_factory.exceptions.exceptions import PluginStorageError

logger = logging.getLogger(__name__)


class PluginFinder(StorageProtocol, FinderManagerProtocol):
    def __init__(self) -> None:
        self._plugins: List[Path] = []

    @property
    def plugins(self) -> Sequence[Path]:
        return self._plugins

    def find_in_directory(
            self,
            storage: FinderStorage
    ) -> None:
        self.__validate_directory(storage.path)
        self.__validate_pattern(storage.pattern)

        try:
            files: List[Path] = list(storage.path.rglob(storage.pattern))
        except (OSError, PermissionError) as exc:
            raise PluginStorageError(
                "Failed to scan plugins directory: '%s'", storage.path
            ) from exc

        for file in files:
            if file.is_file():
                self.__add_file(file)

    def __add_file(self, file: Path) -> None:
        if file in self._plugins:
            logger.warning("Found duplicate plugin file: %s", file)
            return
        self._plugins.append(file)
        logger.debug("Adding plugin file: '%s'", file)

    def __validate_directory(self, directory: Path) -> None:
        if not directory.exists():
            logger.error(
                "Plugins directory does not exist: %s", directory)
            raise PluginStorageError(
                "Plugins directory does not exist: %s", directory)

        if not directory.is_dir():
            logger.error(
                "Plugin path is not a directory: %s", directory)
            raise PluginStorageError(
                "Plugin path is not a directory: %s", directory)

    def __validate_pattern(self, pattern: str) -> None:
        if not isinstance(pattern, str) or not pattern:
            logger.error("Pattern must be a non-empty string")
            raise PluginStorageError("Pattern must be a non-empty string")
