from __future__ import annotations

import logging

from pathlib import Path
from typing import Sequence

from plugin_factory.finder.interface import StorageInterface
from plugin_factory.exceptions.exceptions import PluginStorageError

logger = logging.getLogger(__name__)


class PluginFinder(StorageInterface):
    def __init__(self) -> None:
        self.__plugins: list[Path] = []

    @property
    def plugins(self) -> Sequence[Path]:
        return self.__plugins

    def find_in_directory(
            self,
            plugin_dir: Path,
            pattern: str
    ) -> None:
        logger.debug("Scanning for plugin files in '%s' with pattern '%s'",
                    plugin_dir, pattern)

        if not plugin_dir.exists():
            error_msg = f"Plugins directory does not exist: {plugin_dir}"
            logger.error("Directory not found: '%s'", plugin_dir)
            raise PluginStorageError(error_msg)

        if not plugin_dir.is_dir():
            error_msg = f"Plugin path is not a directory: {plugin_dir}"
            logger.error("Path is not a directory: '%s'", plugin_dir)
            raise PluginStorageError(error_msg)

        files: list[Path] = list(plugin_dir.rglob(pattern))
        logger.info("Found %d plugin files in '%s'", len(files),
                    plugin_dir)

        for file in files:
            self.__add_file(file)

    def find_in_directories(self, directories: list[Path], pattern: str):
        for directory in directories:
            self.find_in_directory(directory, pattern)

    def find_from_json(self, json_file: Path):
        ...

    def find_from_xml(self, xml_file: Path):
        ...

    def find_from_yaml(self, yaml_file: Path):
        ...

    def __add_file(self, file: Path) -> None:
        if file in self.__plugins:
            logger.debug("Found plugin file: %s", file)
            return
        self.__plugins.append(file)
        logger.debug("Adding plugin file: '%s'", file)



