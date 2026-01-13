from __future__ import annotations

import logging
import sys
from importlib import util, machinery
from pathlib import Path
from types import ModuleType

from plugin_factory.contracts import ImporterProtocol
from plugin_factory.exceptions.exceptions import PluginImportError

logger = logging.getLogger(__name__)


class ModuleImporter(ImporterProtocol):
    def import_module(self, plugin: Path) -> ModuleType | None:
        logger.debug("Importing plugin module: %s", plugin)
        try:
            plugin_name: str = self.__generate_module_name(plugin)
            module = self.__import_module_from_file(plugin, plugin_name)
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
            raise PluginImportError(
                "Failed to import plugin: '%s'",
                plugin
            ) from exc

    def __import_module_from_file(
            self,
            plugin: Path,
            module_name: str
    )-> ModuleType:
        spec = util.spec_from_file_location(module_name, plugin)

        if spec is None:
            raise PluginImportError(f"Could not load spec for module: {plugin}")

        if not isinstance(spec.loader, machinery.SourceFileLoader):
            raise PluginImportError(f"Unsupported loader type for: {plugin}")

        module: ModuleType = util.module_from_spec(spec)
        sys.modules[str(plugin)] = module
        spec.loader.exec_module(module)
        module.__file__ = str(plugin)
        module.__name__ = module_name

        return module

    def __generate_module_name(self, plugin: Path) -> str:
        return f"plugin_factory{hash(plugin)}"
