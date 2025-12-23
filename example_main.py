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

    plugin_dir = Path(__file__).parent / "plugins"
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

    manager = PluginManager(plugins)
    manager.init_all()
    manager.get_info()
    manager.start_all()
    manager.get_info()
    manager.stop_all()
    manager.get_info()
    manager.start("Example0")


if __name__ == "__main__":
    main()
