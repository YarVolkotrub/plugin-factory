from src.plugin_loader import PluginLoader
from src.plugin_manager import PluginManager


def main():
    pluginLoader = PluginLoader()
    pluginLoader.load()
    plugins: dict = pluginLoader.get
    print(plugins)

    pluginManager = PluginManager(plugins)
    pluginManager.start('Test')
    pluginManager.stop('Test')


if __name__ == '__main__':
    main()
