from __future__ import annotations

import logging
import sys
from importlib import util
from pathlib import Path
from types import ModuleType

from plugin_factory.contracts import ImporterProtocol
from plugin_factory.exceptions.exceptions import PluginImportError

logger = logging.getLogger(__name__)


class ModuleImporter(ImporterProtocol):
    def import_module(self, plugin: Path) -> ModuleType | None:
        logger.debug("Importing plugin module: %s", plugin)
        try:
            plugin_name: str = f"plugin{hash(plugin)}"
            spec = util.spec_from_file_location(plugin_name,plugin)
            module: ModuleType = util.module_from_spec(spec)
            sys.modules[str(plugin)] = module
            spec.loader.exec_module(module)
            logger.info(
                "Successfully imported plugin module: %s",
                plugin
            )

            return module
        except Exception as exc:
            logger.error(
                "Failed to import plugin module '%s': %s",
                plugin, exc
            )
            raise PluginImportError(plugin) from exc
