import logging
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src import (
    PluginManager,
    PluginLoader,
    LocalStorage,
    FinderLocalPlugin,
    PluginValidator
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def main():
    storage = LocalStorage()
    print(f"Plugin directory: {storage.path}")

    finder = FinderLocalPlugin(storage)
    validator = PluginValidator()

    loader = PluginLoader(finder, validator)
    plugins = loader.load()

    print(f"Loaded {len(plugins)} plugins")
    manager = PluginManager(plugins)
    status = manager.get_status()
    print(f"Plugin statuses: {status}")
    manager.start_all()
    status = manager.get_status()
    print(f"Plugin statuses: {status}")
    manager.stop_all()
    status = manager.get_status()
    print(f"Plugin statuses: {status}")


if __name__ == "__main__":
    main()