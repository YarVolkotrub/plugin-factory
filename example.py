from pluginFactory.plugin_loader import PluginLoader
from pluginFactory.plugin_manager import PluginManager


def main():
    pluginLoader = PluginLoader()
    pluginLoader.load()
    plugins: dict = pluginLoader.get
    print(plugins)

    pluginManager = PluginManager(plugins)
    pluginManager.run('Discord')
    pluginManager.stop('Discord')


if __name__ == '__main__':
    main()
