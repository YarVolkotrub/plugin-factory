from __future__ import annotations

import logging
from pathlib import Path
from types import MappingProxyType, ModuleType
from typing import Sequence, Type, TYPE_CHECKING

from plugin_factory.contracts import PluginLoaderProtocol

if TYPE_CHECKING:
    from plugin_factory.core import PluginBase
    from plugin_factory.contracts import (
        PluginValidatorProtocol,
        StorageProtocol,
        InstanceProtocol,
        ClassScannerProtocol,
        ImporterProtocol,
    )

logger = logging.getLogger(__name__)


class PluginLoader(PluginLoaderProtocol):
    def __init__(
        self,
        storage: StorageProtocol,
        validator: PluginValidatorProtocol,
        importer: ImporterProtocol,
        class_scanner: ClassScannerProtocol,
        factory: InstanceProtocol,
    ) -> None:
        self._storage = storage
        self._validator = validator
        self._importer = importer
        self._class_scanner = class_scanner
        self._factory = factory
        self._plugins: dict[str, PluginBase] = {}

        logger.debug("Initialized %s", self.__class__.__name__)

    def load(self) -> MappingProxyType[str, PluginBase]:
        logger.info("Starting plugin loading process")

        plugins: Sequence[Path] = self._storage.plugins
        logger.debug("Found %d file(s) to scan", len(plugins))

        for plugin in plugins:
            module: ModuleType | None = self._importer.import_module(plugin)

            if module is None:
                continue

            cls: Type[PluginBase] | None = self._class_scanner.get_class(module)

            if cls is None:
                continue

            plugin_instance: PluginBase = self._factory.get_instance(cls)

            if plugin_instance is None:
                continue

            if not self._validator.is_valid(plugin_instance, self._plugins):
                # TODO: unload instance
                continue

            self._plugins[plugin_instance.info.name] = plugin_instance

        logger.info("Plugin loading completed, total %d",
                    len(self._plugins))
        return MappingProxyType(self._plugins)
