from __future__ import annotations

import logging

from types import MappingProxyType, ModuleType
from typing import Sequence, Type, TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    from .module_importer import ModuleImporter
    from .plugin_class_scanner import PluginClassScanner
    from .factory_plugin import FactoryPlugin
    from plugin_factory.domain.plugin_base import PluginBase
    from plugin_factory.validation.interface.validator import \
        PluginValidatorInterface
    from plugin_factory.finder.interface.storage_interface import \
        StorageInterface

logger = logging.getLogger(__name__)


class PluginLoader:
    def __init__(
        self,
        storage: StorageInterface,
        validator: PluginValidatorInterface,
        importer: ModuleImporter,
        class_finder: PluginClassScanner,
        factory: FactoryPlugin,
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

        plugins: Sequence[Path] = self._storage.plugins
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
