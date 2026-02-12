from __future__ import annotations

from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, Dict, Sequence, Optional

from plugin_factory.core import FinderStorage, FSM_TRANSITIONS
from plugin_factory.infrastructure import (
    PluginInstanceFactory,
    ImportlibModuleImporter,
    PluginLoader,
    ClassExtractor,
    PluginLifecycleController,
    PluginFinder,
)

if TYPE_CHECKING:
    from plugin_factory.core.plugins.plugin_base import PluginBase
    from plugin_factory.interfaces import (
        ImporterProtocol,
        ClassExtractorProtocol,
        PluginInstanceProtocol,
    )


class PluginFactoryManager:
    def __init__(
            self,
            storage: Optional[FinderStorage] | None = None,
            importer: Optional[ImporterProtocol] = None,
            class_scanner: Optional[ClassExtractorProtocol] = None,
            factory: Optional[PluginInstanceProtocol] = None
    ) -> None:
        if storage is not None and not isinstance(storage, FinderStorage):
            raise TypeError(
                f"storage must be FinderStorage or None, "
                f"got {type(storage).__name_}"
            )

        self._lifecycle: PluginLifecycleController = PluginLifecycleController(FSM_TRANSITIONS)
        self._storage = storage
        self._finder = PluginFinder()
        self._plugins: Dict[str, PluginBase] = {}

        self._importer = importer or ImportlibModuleImporter()
        self._class_scanner = class_scanner or ClassExtractor()
        self._factory = factory or PluginInstanceFactory()

    @property
    def lifecycle(self) -> PluginLifecycleController:
        return self._lifecycle

    @property
    def plugins(self) -> MappingProxyType[str, PluginBase]:
        if not self._plugins:
            raise RuntimeError("Plugins not loaded. Call load() first.")

        return MappingProxyType(self._plugins)

    def setup(self, storage: FinderStorage) -> PluginFactoryManager:
        if storage.path is None or not storage.path.exists():
            raise ValueError(f"Invalid storage path: {storage}")

        self._storage = storage

        return self

    def discover(self) -> Sequence[Path]:
        if not self._storage:
            raise ValueError(
                "Plugin configuration not set. Call setup() first.")

        if self._finder is None:
            raise RuntimeError("Plugin finder not initialized")

        storage: FinderStorage = FinderStorage(
            path=self._storage.path,
            pattern=self._storage.pattern
        )

        self._finder.find_in_directory(storage)
        plugins: Sequence[Path] = self._finder.plugins

        return plugins

    def load(self) -> MappingProxyType[str, PluginBase]:
        if self._finder is None:
            raise RuntimeError("Plugin finder not initialized")

        if not self._finder.plugins:
            raise ValueError("No plugins found. Call discover() first.")

        try:
            loader = PluginLoader(
                storage=self._finder,
                importer=self._importer,
                class_extractor=self._class_scanner,
                factory=self._factory
            )

            self._plugins = dict(loader.load())

            return MappingProxyType(self._plugins)

        except Exception as exc:
            raise RuntimeError(f"Plugin loading failed: {exc}") from exc
