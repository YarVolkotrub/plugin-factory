from __future__ import annotations

import logging
from pathlib import Path
from typing import Sequence, List

from plugin_factory.interfaces import PluginDiscoveryProtocol, PluginStorageProtocol
from plugin_factory.core import FinderStorage
from plugin_factory.exceptions import PluginStorageError

logger = logging.getLogger(__name__)


class PluginFinder(PluginStorageProtocol, PluginDiscoveryProtocol):
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
                f"Failed to scan plugins directory: '{storage}'") from exc

        for file in files:
            if file.is_file():
                self.__add_file(file)

        logger.debug(f"Found {len(self._plugins)} plugin file(s)")

    def __add_file(self, file: Path) -> None:
        if file in self._plugins:
            logger.warning(f"Found duplicate plugin file: '{file}'")
            return
        self._plugins.append(file)
        logger.debug(f"Adding plugin file: '{file}'")

    def __validate_directory(self, directory: Path) -> None:
        if not directory.exists():
            raise PluginStorageError(
                f"Plugins directory does not exist: '{directory}'")

        if not directory.is_dir():
            raise PluginStorageError(
                f"Plugin path is not a directory: '{directory}'")

    def __validate_pattern(self, pattern: str) -> None:
        if not isinstance(pattern, str) or not pattern:
            raise PluginStorageError("Pattern must be a non-empty string")
