class PluginManager(object):
    def __init__(self, plugins: dict):
        self.__plugins: dict = plugins

    def start(self, pluginName: str) -> None:
        if not self.__isCorrectName(pluginName):
            raise Exception("Plugin not found")
        return self.__plugins.get(pluginName).start()

    def stop(self, pluginName: str) -> None:
        if not self.__isCorrectName(pluginName):
            raise Exception("Plugin not found")
        return self.__plugins.get(pluginName).stop()

    def __isCorrectName(self, pluginName: str) -> bool:
        return pluginName in self.__plugins
