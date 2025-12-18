import logging
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src import (
    PluginManager,
    PluginLoader,
    LocalStorage,
    LocalPluginFinder,
    PluginValidator,
    PluginClassFinder,
    ModuleImporter,
    PluginFactory
)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def main():
    from pathlib import Path

    plugin_dir = Path(__file__).parent / "src" / "plugins"
    pattern = "plugin*.py"

    storage = LocalStorage(plugin_dir, pattern)
    finder = LocalPluginFinder()
    validator = PluginValidator()

    loader = PluginLoader(
        storage=storage,
        finder=finder,
        validator=validator,
        importer=ModuleImporter(),
        class_finder=PluginClassFinder(),
        factory=PluginFactory(),
    )
    plugins = loader.load()

    print(f"Loaded {len(plugins)} plugins")
    manager = PluginManager(plugins)
    info = manager.get_info()
    print(f"Plugin info: {info}")
    manager.start_all()
    info = manager.get_info()
    print(f"Plugin info: {info}")
    print(f"Plugin info: {manager.get_states()}")
    manager.stop_all()
    info = manager.get_info()
    print(f"Plugin info: {info}")

    print(f"Plugin info: {manager.get_states()}")

if __name__ == "__main__":
    main()
