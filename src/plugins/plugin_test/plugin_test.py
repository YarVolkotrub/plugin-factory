from src.basePlugin import BasePlugin


class PluginOne(BasePlugin):
    def __init__(self):
        self.__name = "Test"

    @property
    def getName(self):
        return self.__name

    def start(self):
        print("start plugin")

    def stop(self):
        print("stop plugin")
