from __future__ import annotations

import logging
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, Dict, Sequence, Optional

from plugin_factory.core import FinderStorage, FSMTransition
from plugin_factory.infrastructure import (
    FactoryPlugin,
    ModuleImporter,
    PluginLoader,
    PluginClassScanner,
    StructuralPluginValidator,
    LifecycleManager,
    PluginFinder,
)

if TYPE_CHECKING:
    from plugin_factory.core.plugins.plugin_base import PluginBase
    from plugin_factory.contracts import (
        TransitionProtocol,
        ImporterProtocol,
        PluginValidatorProtocol,
        ClassScannerProtocol,
        InstanceProtocol,
    )

logger = logging.getLogger(__name__)


class Lifecycle:
    def __init__(self):
        self._state_transitions: TransitionProtocol = FSMTransition()
        self._lifecycle: LifecycleManager = LifecycleManager(self._state_transitions)

    @property
    def execute(self) -> LifecycleManager:
        return self._lifecycle


class PluginManager:
    def __init__(
            self,
            storage: Optional[FinderStorage] | None = None,
            validator: Optional[PluginValidatorProtocol] = None,
            importer: Optional[ImporterProtocol] = None,
            class_scanner: Optional[ClassScannerProtocol] = None,
            factory: Optional[InstanceProtocol] = None
    ) -> None:
        if storage is not None and not isinstance(storage, FinderStorage):
            raise TypeError(
                "storage must be FinderStorage or None, got %r",
                type(storage).__name__
            )

        self._storage = storage
        self._finder = PluginFinder()
        self._plugins: Dict[str, PluginBase] = {}

        self._validator = validator or StructuralPluginValidator()
        self._importer = importer or ModuleImporter()
        self._class_scanner = class_scanner or PluginClassScanner()
        self._factory = factory or FactoryPlugin()

        logger.debug("PluginManager initialized")

    def setup(self, storage: FinderStorage) -> PluginManager:
        if storage.path is None or not storage.path.exists():
            raise ValueError(f"Invalid storage path: {storage.path}")

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
                validator=self._validator,
                importer=self._importer,
                class_scanner=self._class_scanner,
                factory=self._factory
            )

            self._plugins = dict(loader.load())

            return MappingProxyType(self._plugins)

        except Exception as exc:
            raise RuntimeError(f"Plugin loading failed: %s", exc) from exc

    @property
    def plugins(self) -> MappingProxyType[str, PluginBase]:
        if not self._plugins:
            raise RuntimeError("Plugins not loaded. Call load() first.")

        return MappingProxyType(self._plugins)
