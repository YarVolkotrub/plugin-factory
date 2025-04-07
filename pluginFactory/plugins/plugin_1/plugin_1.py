from pluginFactory.basePlugin import BasePlugin


class PluginOne(BasePlugin):
    def __init__(self):
        self.__name = "Discord"

    @property
    def getName(self):
        return self.__name

    def run(self):
        print("run Discord")

    def stop(self):
        print("stop Discord")
