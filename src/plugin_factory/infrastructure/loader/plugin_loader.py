from __future__ import annotations

import logging
from pathlib import Path
from types import MappingProxyType, ModuleType
from typing import Sequence, Type, TYPE_CHECKING, Dict

from plugin_factory.contracts import PluginLoaderProtocol

if TYPE_CHECKING:
    from plugin_factory.core import PluginBase
    from plugin_factory.contracts import (
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
        importer: ImporterProtocol,
        class_scanner: ClassScannerProtocol,
        factory: InstanceProtocol,
    ) -> None:
        self._storage = storage
        self._importer = importer
        self._class_scanner = class_scanner
        self._factory = factory
        self._plugins: Dict[str, PluginBase] = {}

        logger.debug("Initialized %s", self.__class__.__name__)

    def load(self) -> MappingProxyType[str, PluginBase]:
        plugins: Sequence[Path] = self._storage.plugins
        logger.info("Found %d file(s) to scan", len(plugins))

        for plugin in plugins:
            logger.debug("Importing plugin module: '%s'", plugin)
            module: ModuleType = self._importer.import_module(plugin)

            cls: Type[PluginBase]  = self._class_scanner.get_class(module)
            plugin_instance: PluginBase = self._factory.get_instance(cls)

            self._plugins[plugin_instance.info.name] = plugin_instance

        logger.info("Plugin loading completed, total %d",
                    len(self._plugins))

        return MappingProxyType(self._plugins)
