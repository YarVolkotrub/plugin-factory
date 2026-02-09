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
        ClassExtractorProtocol,
        ImporterProtocol,
    )

logger = logging.getLogger(__name__)


class PluginLoader(PluginLoaderProtocol):
    def __init__(
        self,
        storage: StorageProtocol,
        importer: ImporterProtocol,
        class_extractor: ClassExtractorProtocol,
        factory: InstanceProtocol,
    ) -> None:
        self._storage = storage
        self._importer = importer
        self._class_extractor = class_extractor
        self._factory = factory
        self._plugins: Dict[str, PluginBase] = {}

        logger.debug(f"Initialized {self.__class__.__name__}")

    def load(self) -> MappingProxyType[str, PluginBase]:
        plugins: Sequence[Path] = self._storage.plugins
        logger.info(f"Found {len(plugins)} file(s) to scan")

        for plugin in plugins:
            logger.debug(f"Importing plugin module: '{plugin}'")
            module: ModuleType = self._importer.import_module(plugin)

            cls: Type[PluginBase]  = self._class_extractor.extract_plugin_class(module)
            plugin_instance: PluginBase = self._factory.get_instance(cls)

            self._plugins[plugin_instance.info.name] = plugin_instance

        logger.info(f"Plugin loading completed, total {len(self._plugins)}"                    )

        return MappingProxyType(self._plugins)
