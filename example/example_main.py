import logging
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from plugin_factory import Loader, Finder, Lifecycle


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def main():
    plugin_dir = Path(__file__).parent / "plugins"
    pattern = "plugin*.py"

    finder = Finder()
    finder.find_plugins(plugin_dir, pattern)

    loader = Loader(finder.execute)
    plugins = loader.plugins

    lifecycle_manager = Lifecycle()
    manager = lifecycle_manager.execute

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
