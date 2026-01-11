from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING

from plugin_factory.core.state_machine.transition import Transition
from plugin_factory.infrastructure.finder.plugin_finder import PluginFinder
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
        StorageProtocol,
        FinderPath,
        PluginLoaderProtocol,
        TransitionProtocol
    )


# TODO: временное решение
class Loader:
    def __init__(self, plugins: StorageProtocol):
        self._loader: PluginLoaderProtocol = PluginLoader(
            storage=plugins,
            validator=StructuralPluginValidator(),
            importer=ModuleImporter(),
            class_scanner=PluginClassScanner(),
            factory=FactoryPlugin(),
        )

    @property
    def plugins(self) -> MappingProxyType[str, PluginBase]:
        return self._loader.load()

class Finder:
    def __init__(self):
        self._finder: FinderPath = PluginFinder()

    @property
    def execute(self):
        return self._finder

    def find_plugins(self,
            plugin_dir: Path,
            pattern: str
        ):
        self._finder.find_in_directory(plugin_dir, pattern)

class Lifecycle:
    def __init__(self):
        self._state_transitions: TransitionProtocol = Transition()
        self._lifecycle: LifecycleManager = LifecycleManager(self._state_transitions)

    @property
    def execute(self) -> LifecycleManager:
        return self._lifecycle
