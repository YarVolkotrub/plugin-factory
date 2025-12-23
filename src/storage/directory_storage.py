from pathlib import Path
from typing import Sequence
import logging

from ..interfaces.plugin_storage import PluginStorageBase
from ..exceptions import PluginStorageError

logger = logging.getLogger(__name__)


class DirectoryPluginStorage(PluginStorageBase):
    def __init__(
        self,
        plugin_dir: Path,
        pattern: str
    ) -> None:
        logger.debug("Initialized %s with directory: '%s', pattern: '%s'",
                    self.__class__.__name__, plugin_dir, pattern)

        self._plugin_dir = plugin_dir
        self._pattern = pattern

    def get_files(self) -> Sequence[Path]:
        logger.debug("Scanning for plugin files in '%s' with pattern '%s'",
                    self._plugin_dir, self._pattern)

        if not self._plugin_dir.exists():
            error_msg = f"Plugins directory does not exist: {self._plugin_dir}"
            logger.error("Directory not found: '%s'", self._plugin_dir)
            raise PluginStorageError(error_msg)

        if not self._plugin_dir.is_dir():
            error_msg = f"Plugin path is not a directory: {self._plugin_dir}"
            logger.error("Path is not a directory: '%s'", self._plugin_dir)
            raise PluginStorageError(error_msg)

        files: list[Path] = list(self._plugin_dir.rglob(self._pattern))
        logger.info("Found %d plugin files in '%s'", len(files),
                    self._plugin_dir)

        if logger.isEnabledFor(logging.DEBUG) and files:
            for file in files:
                logger.debug("Found plugin file: %s", file)

        return files
