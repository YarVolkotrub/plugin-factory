from pathlib import Path
from typing import Sequence
import logging

from src.interfaces.plugin_storage import PluginStorageBase
from src.exceptions import PluginStorageError

logger = logging.getLogger(__name__)


class DirectoryPluginStorage(PluginStorageBase):
    def __init__(
        self,
        plugin_dir: Path,
        pattern: str
    ) -> None:
        logger.debug(f"init {__class__.__name__}")

        self._plugin_dir = plugin_dir
        self._pattern = pattern

    def get_files(self) -> Sequence[Path]:
        if not self._plugin_dir.exists():
            raise PluginStorageError(
                f"Plugins directory does not exist: {self._plugin_dir}"
            )

        files: list[Path] = list(self._plugin_dir.rglob(self._pattern))

        return files
