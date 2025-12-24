from __future__ import annotations
import logging
from types import MappingProxyType, ModuleType
from typing import Sequence, Type
from pathlib import Path

from ..domain.plugin import PluginBase
from ..interfaces.plugin_loader import PluginLoaderBase
from ..interfaces.validator import PluginValidatorBase
from ..interfaces.plugin_storage import PluginStorageBase
from ..lifecycle.module_importer import ModuleImporter
from ..lifecycle.plugin_class_finder import PluginClassScanner
from ..lifecycle.plugin_factory import PluginFactory

logger = logging.getLogger(__name__)


class PluginLoader(PluginLoaderBase):
    def __init__(
        self,
        storage: PluginStorageBase,
        validator: PluginValidatorBase,
        importer: ModuleImporter,
        class_finder: PluginClassScanner,
        factory: PluginFactory,
    ) -> None:
        self._storage = storage
        self._validator = validator
        self._importer = importer
        self._class_finder = class_finder
        self._factory = factory
        self._plugins: dict[str, PluginBase] = {}

        logger.debug("Initialized %s", self.__class__.__name__)
        logger.debug("Components: storage=%s, finder=%s, validator=%s, importer=%s, "
                    "class_finder=%s, factory=%s",
                    storage.__class__.__name__,
                    validator.__class__.__name__,
                    importer.__class__.__name__,
                    class_finder.__class__.__name__,
                    factory.__class__.__name__)

    def load(self) -> MappingProxyType[str, PluginBase]:
        logger.info("Starting plugin loading process")

        plugins: Sequence[Path] = self._storage.get_files()
        logger.debug("Found %d file(s) to scan", len(plugins))

        for plugin in plugins:
            module: ModuleType | None = self._importer.import_module(plugin)

            if module is None:
                continue

            cls: Type[PluginBase] | None = self._class_finder.get(module)

            if cls is None:
                logger.debug("No plugin class found in module: %s", plugin)
                continue

            plugin_instance = self._factory.create(cls)

            if plugin_instance is None:
                logger.warning("Failed to create instance for plugin: %s",
                               plugin)
                continue

            if not self._validator.is_valid(plugin_instance, self._plugins):
                logger.warning("Plugin validation failed: %s", plugin)
                continue

            self._plugins[plugin_instance.info.name] = plugin_instance

        logger.info("Plugin loading completed, total %d",
                    len(self._plugins))
        return MappingProxyType(self._plugins)
