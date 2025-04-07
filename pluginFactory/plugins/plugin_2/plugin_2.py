from pluginFactory.basePlugin import BasePlugin


class PluginTwo(BasePlugin):
    def __init__(self):
        self.__name = "Telegram"

    @property
    def getName(self):
        return self.__name

    def run(self):
        print("run Telegram")

    def stop(self):
        print("stop Telegram")
