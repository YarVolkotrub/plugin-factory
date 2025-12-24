from __future__ import annotations

import sys
from importlib import util
from pathlib import Path
from types import ModuleType
import logging


from ..exceptions import PluginImportError

logger = logging.getLogger(__name__)


class ModuleImporter:
    def import_module(self, plugin: Path) -> ModuleType | None:
        logger.debug("Importing plugin module: %s", plugin)
        try:
            plugin_name = f"plugin_{hash(plugin)}"
            spec = util.spec_from_file_location(plugin_name,plugin)
            module = util.module_from_spec(spec)
            sys.modules[str(plugin)] = module
            spec.loader.exec_module(module)
            logger.info("Successfully imported plugin module: %s", plugin)

            return module
        except Exception as exc:
            logger.error("Failed to import plugin module '%s': %s", plugin, exc)
            raise PluginImportError(plugin) from exc
