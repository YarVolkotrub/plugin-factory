from pathlib import Path
from typing import Sequence
import logging

from ..interfaces.plugin_storage import PluginStorageBase
from ..exceptions import PluginStorageError

logger = logging.getLogger(__name__)


class LocalStorage(PluginStorageBase):
    def __init__(
        self,
        plugin_dir: Path,
        pattern: str
    ) -> None:
        self._plugin_dir = plugin_dir
        self._pattern = pattern
        logger.debug(f"init {__class__.__name__}")

    def get(self) -> Sequence[Path]:
        if not self._plugin_dir.exists():
            raise PluginStorageError(
                f"Plugins directory does not exist: {self._plugin_dir}"
            )

        return list(self._plugin_dir.rglob(self._pattern))
