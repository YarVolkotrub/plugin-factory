from __future__ import annotations

import logging
import sys
import uuid
from importlib import util
from pathlib import Path
from types import ModuleType

from plugin_factory.contracts import ImporterProtocol
from plugin_factory.exceptions import PluginImportError, PluginStorageError

logger = logging.getLogger(__name__)


class ModuleImporter(ImporterProtocol):
    def import_module(self, plugin: Path) -> ModuleType:
        try:
            plugin_name: str = self.__generate_module_name(plugin)
            module = self.__import_module_from_file(plugin, plugin_name)

            return module
        except Exception as exc:
            logger.error(
                "Failed to import plugin module '%s': '%s'",
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
        try:
            spec = util.spec_from_file_location(module_name, plugin)
        except (ImportError, FileNotFoundError) as exc:
            raise PluginStorageError(
                "Failed to create import spec for '%s'", plugin
            ) from exc

        if spec is None or spec.loader is None:
            raise PluginStorageError(
                f"Invalid import spec for plugin file: '%s'", plugin)

        try:
            module: ModuleType = util.module_from_spec(spec)
            plugin: str = str(plugin)
            sys.modules[plugin] = module
            spec.loader.exec_module(module)
            module.__file__  = plugin
            module.__name__ = module_name

            return module
        except (SyntaxError,
                ImportError,
                FileNotFoundError,
                AttributeError) as exc:
            raise PluginImportError(
                "Failed to import plugin module: '%s'", plugin
            ) from exc

    def __generate_module_name(self, plugin: Path) -> str:
        return f"plugin_factory.plugins.{plugin.stem}_{uuid.uuid4().hex}"
