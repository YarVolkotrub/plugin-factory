from src.plugin_loader import PluginLoader
from src.plugin_manager import PluginManager


def main():
    pluginLoader: PluginLoader = PluginLoader()
    pluginLoader.load()
    plugins: dict = pluginLoader.plugins
    print(plugins)

    pluginManager: PluginManager = PluginManager(plugins)
    pluginManager.start('Test')
    pluginManager.stop('Test')
    pluginManager.stop_all()
    pluginManager.start_all()
    print(pluginManager.get_status())


if __name__ == '__main__':
    main()
