import logging
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, Dict, Sequence, Optional

from plugin_factory.core.finder.finder_storage import FinderStorage
from plugin_factory.core.state_machine.transition import Transition
from plugin_factory.infrastructure.finder.plugin_finder import \
    PluginFinder
from plugin_factory.infrastructure.louder.factories.factory_plugin import \
    FactoryPlugin
from plugin_factory.infrastructure.louder.importers.module_importer import \
    ModuleImporter
from plugin_factory.infrastructure.louder.plugin_loader import PluginLoader
from plugin_factory.infrastructure.louder.scanners.plugin_class_scanner import \
    PluginClassScanner
from plugin_factory.infrastructure.louder.validators.plugin_config_validator import \
    StructuralPluginValidator
from plugin_factory.infrastructure.state_machine.lifecycle_manager import \
    LifecycleManager

if TYPE_CHECKING:
    from plugin_factory.core.plugins.plugin_base import PluginBase
    from plugin_factory.contracts import (
        TransitionProtocol
    )

logger = logging.getLogger(__name__)


class Lifecycle:
    def __init__(self):
        self._state_transitions: TransitionProtocol = Transition()
        self._lifecycle: LifecycleManager = LifecycleManager(self._state_transitions)

    @property
    def execute(self) -> LifecycleManager:
        return self._lifecycle


class PluginManager:
    def __init__(
            self,
            storage: FinderStorage | None = None,
            validator: Optional[StructuralPluginValidator] = None,
            importer: Optional[ModuleImporter] = None,
            class_scanner: Optional[PluginClassScanner] = None,
            factory: Optional[FactoryPlugin] = None
    ) -> None:
        self._storage = storage
        self._finder = PluginFinder()
        self._loader = None
        self._plugins: Dict[str, PluginBase] = {}

        self._validator = validator or StructuralPluginValidator()
        self._importer = importer or ModuleImporter()
        self._class_scanner = class_scanner or PluginClassScanner()
        self._factory = factory or FactoryPlugin()

        logger.debug("PluginManager initialized")

    def setup(self, storage: FinderStorage) -> PluginManager:
        self._storage = storage
        return self

    def discover(self) -> Sequence[Path]:
        if not self._storage:
            raise ValueError(
                "Plugin configuration not set. Call setup() first.")

        storage = FinderStorage(
            path=self._storage.path,
            pattern=self._storage.pattern
        )

        self._finder.find_in_directory(storage)
        return self._finder.plugins

    def load(self) -> MappingProxyType[str, PluginBase]:
        if not self._finder.plugins:
            raise ValueError("No plugins found. Call discover() first.")

        self._loader = PluginLoader(
            storage=self._finder,
            validator=self._validator,
            importer=self._importer,
            class_scanner=self._class_scanner,
            factory=self._factory
        )

        self._plugins = dict(self._loader.load())
        return MappingProxyType(self._plugins)

    @property
    def plugins(self) -> MappingProxyType[str, PluginBase]:
        return MappingProxyType(self._plugins)
