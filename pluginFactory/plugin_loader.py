import importlib.util
import os
from glob import glob

from pluginFactory.basePlugin import BasePlugin


class PluginLoader:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)

        return cls.instance

    def __init__(self):
        self.__pluginTemplate: str = '/*/plugin*.py'
        self.__dirWithPlugins: str = 'plugins'
        self.__plugins: dict = {}
        self.__basePlugin = BasePlugin

    @property
    def get(self) -> dict:
        return self.__plugins

    def load(self) -> None:
        pathToPlugins: str = self.__getPath(self.__dirWithPlugins,
                                            self.__pluginTemplate)

        for plugin in [file for file in glob(pathToPlugins)]:
            pluginName: str = self.__getFullName(plugin,
                                                 self.__dirWithPlugins)
            self.__import(pluginName)

        self.__initiate()

    def __import(self, plugin: str) -> None:
        try:
            importlib.import_module(plugin)
        except Exception as ex:
            print(f"Couldn't import plugin - {plugin} - {ex}")

    def __initiate(self) -> None:
        for plugin in self.__basePlugin.__subclasses__():
            if self.__isCorrectBasePlugin(plugin):
                p: BasePlugin = plugin()
                self.__plugins.update({p.getName: p})

    def __isCorrectBasePlugin(self, plugin: type[BasePlugin]) -> bool:
        basePluginRun: str = "run"
        basePluginStop: str = "stop"

        return hasattr(plugin, basePluginRun) \
                and hasattr(plugin, basePluginStop)

    def __getPath(self, dirWithPlugin: str, nameTemplate: str) -> str:
        return os.path.abspath(
            os.path.realpath(os.path.dirname(__file__)
                + "/" + dirWithPlugin)) + nameTemplate

    def __getFullName(self, plugin: str, dirWithPlugins: str) -> str:
        lengthTypeFile: int = len('.py')

        pluginName: str = os.path.basename(
            os.path.abspath(os.path.realpath(plugin)))[:-lengthTypeFile]
        pluginDir: str = os.path.basename(
            os.path.dirname(os.path.abspath(
                os.path.realpath(plugin))))
        pathToLocal: str = os.path.basename(os.path.dirname(__file__))

        return (f"{pathToLocal}"
                f".{dirWithPlugins}"
                f".{pluginDir}"
                f".{pluginName}")
