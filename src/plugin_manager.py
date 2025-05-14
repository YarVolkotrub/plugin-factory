class PluginManager(object):
    def __init__(self, plugins: dict):
        self.__plugins: dict = plugins

    def start(self, plugin_name: str) -> None:
        if not self.__is_correct_name(plugin_name):
            raise Exception(f"Don't start, plugin {plugin_name} not found")
        return self.__plugins.get(plugin_name).start()

    def stop(self, plugin_name: str) -> None:
        if not self.__is_correct_name(plugin_name):
            raise Exception(f"Don't stop, plugin {plugin_name} not found")
        return self.__plugins.get(plugin_name).stop()

    def __is_correct_name(self, plugin_name: str) -> bool:
        return plugin_name in self.__plugins
