class PluginManager(object):
    def __init__(self, plugins: dict):
        self.__plugins: ReadOnly[dict] = plugins

    def run(self, pluginName: str) -> None:
        if not self.__isCorrectName(pluginName):
            return
        return self.__plugins.get(pluginName).run()

    def stop(self, pluginName: str) -> None:
        if not self.__isCorrectName(pluginName):
            return
        return self.__plugins.get(pluginName).stop()

    def __isCorrectName(self, pluginName: str) -> bool:
        return pluginName in self.__plugins

