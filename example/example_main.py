import logging
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src import (
    PluginStateManager,
    PluginLoader,
    DirectoryPluginStorage,
    StructuralPluginValidator,
    PluginClassScanner,
    ModuleImporter,
    PluginFactory
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def main():
    from pathlib import Path

    plugin_dir = Path(__file__).parent  /"plugins"
    pattern = "plugin*.py"

    storage = DirectoryPluginStorage(plugin_dir, pattern)
    validator = StructuralPluginValidator()

    loader = PluginLoader(
        storage=storage,
        validator=validator,
        importer=ModuleImporter(),
        class_finder=PluginClassScanner(),
        factory=PluginFactory(),
    )
    plugins = loader.load()

    manager = PluginStateManager(plugins)
    manager.init_all_plugin()
    manager.get_plugin_info()
    manager.start_all_plugin()
    manager.get_plugin_info()
    manager.stop_all_plugin()
    manager.get_plugin_info()
    manager.start_plugin("Example0")
    manager.start_plugin("Example0")

if __name__ == "__main__":
    main()
