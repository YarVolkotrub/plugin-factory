from __future__ import annotations
import logging
from types import MappingProxyType, ModuleType
from typing import Sequence, Type
from pathlib import Path

from ..interfaces.plugin import PluginBase
from ..interfaces.plugin_loader import PluginLoaderBase
from ..interfaces.validator import PluginValidatorBase
from ..interfaces.finder import PluginFinderBase
from ..interfaces.plugin_storage import PluginStorageBase
from ..loader.importer import ModuleImporter
from ..loader.class_finder import PluginClassFinder
from ..loader.factory import PluginFactory

logger = logging.getLogger(__name__)


class PluginLoader(PluginLoaderBase):
    def __init__(
        self,
        storage: PluginStorageBase,
        finder: PluginFinderBase,
        validator: PluginValidatorBase,
        importer: ModuleImporter,
        class_finder: PluginClassFinder,
        factory: PluginFactory,
    ) -> None:
        self._storage = storage
        self._finder = finder
        self._validator = validator
        self._importer = importer
        self._class_finder = class_finder
        self._factory = factory
        self._plugins: dict[str, PluginBase] = {}
        logger.debug(f"init {__class__.__name__}")

    def load(self) -> MappingProxyType[str, PluginBase]:
        files: Sequence[Path] = self._storage.get_files()
        plugins: Sequence[str] = self._finder.get(files)

        for plugin in plugins:
            module: ModuleType | None = self._importer.import_module(plugin)

            if module is None:
                continue

            cls: Type[PluginBase] | None = self._class_finder.get(module)

            if cls is None:
                continue

            instance = self._factory.create(cls)

            if instance is None:
                continue

            if not self._validator.is_valid(instance, self._plugins):
                continue

            self._plugins[instance.name] = instance

        return MappingProxyType(self._plugins)
