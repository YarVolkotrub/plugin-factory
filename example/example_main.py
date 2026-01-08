import logging
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from plugin_factory import PluginLoader
from plugin_factory import PluginFinder
from plugin_factory import StructuralPluginValidator
from plugin_factory import PluginClassScanner
from plugin_factory import ModuleImporter
from plugin_factory import FactoryPlugin
from plugin_factory import PluginStateTransitions
from plugin_factory import PluginStateManager


# from plugin_factory import (
#     PluginLoader,
#     PluginFinder,
#     StructuralPluginValidator,
#     PluginClassScanner,
#     ModuleImporter,
#     FactoryPlugin,
#     PluginStateTransitions,
#     PluginStateManager,
# )

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def main():
    plugin_dir = Path(__file__).parent / "plugins"
    pattern = "plugin*.py"

    finder = PluginFinder()
    finder.find_in_directory(plugin_dir, pattern)

    validator = StructuralPluginValidator()

    loader = PluginLoader(
        storage=finder,
        validator=validator,
        importer=ModuleImporter(),
        class_scanner=PluginClassScanner(),
        factory=FactoryPlugin(),
    )
    plugins = loader.load()

    state_transitions = PluginStateTransitions()
    manager = PluginStateManager(state_transitions)

    manager.add_plugins(plugins)
    manager.init_all_plugin()
    manager.get_plugin_info()
    manager.start_all_plugin()
    manager.get_plugin_info()
    manager.stop_all_plugin()
    manager.get_plugin_info()
    manager.start_plugin("Example0")
    manager.start_plugin("Example0")
    print(manager.get_plugin_states())
    print(manager.get_plugin_info())

if __name__ == "__main__":
    main()
