from __future__ import annotations
from importlib import import_module
from types import ModuleType
import logging
from pathlib import Path

from ..exceptions import PluginImportError

logger = logging.getLogger(__name__)


class ModuleImporter:
    def import_module(self, plugin: str) -> ModuleType | None:
        try:
            module = import_module(plugin)
            logger.debug(f"Plugin '{plugin}' import - success")
            return module
        except Exception as exc:
            logger.error(f"Plugin '{plugin}' import - failed")
            raise PluginImportError(plugin) from exc
