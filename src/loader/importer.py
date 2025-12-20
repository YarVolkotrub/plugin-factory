from __future__ import annotations
from importlib import import_module
from types import ModuleType
import logging
from pathlib import Path

from ..exceptions import PluginImportError

logger = logging.getLogger(__name__)


class ModuleImporter:
    def import_module(self, import_path: Path) -> ModuleType | None:
        try:
            module = import_module(import_path)
            logger.debug(f"Plugin '{import_path}' import - success")
            return module
        except Exception as exc:
            logger.error(f"Plugin '{import_path}' import - failed")
            raise PluginImportError(import_path) from exc
