from pathlib import Path
from typing import Sequence

from ..interfaces.plugin_storage import PluginStorageBase
from ..exceptions import PluginStorageError

class LocalStorage(PluginStorageBase):
    def __init__(
        self,
        plugin_dir: Path,
        pattern: str = "plugin*.py"
    ) -> None:
        self._plugin_dir = plugin_dir
        self._pattern = pattern

    def get(self) -> Sequence[Path]:
        if not self._plugin_dir.exists():
            raise PluginStorageError(
                f"Plugins directory does not exist: {self._plugin_dir}"
            )

        return list(self._plugin_dir.rglob(self._pattern))
