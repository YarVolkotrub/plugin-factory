import logging
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from plugin_factory import FinderStorage, PluginManager


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def main():
    plugin_dir = Path(__file__).parent / "plugins"
    pattern = "plugin*.py"

    plugin_files = FinderStorage(pattern, plugin_dir)
    plugin_manager = PluginManager(storage=plugin_files)
    # plugin_manager = PluginManager()
    # plugin_manager.setup(plugin_files)
    plugin_manager.discover()
    plugin_manager.load()
    plugins = plugin_manager.plugins

    manager = plugin_manager.lifecycle

    manager.add_plugins(plugins)
    manager.init_all_plugin()
    manager.get_plugin_info()
    manager.start_all_plugin()
    manager.get_plugin_info()
    manager.stop_all_plugin()
    manager.get_plugin_info()
    print(manager.get_plugin_states())
    print(manager.get_plugin_info())
    print(manager.get_plugin_has_error())
    print(manager.get_plugins_error())

if __name__ == "__main__":
    main()
