from . import glob, import_module, path 

from . import Plugin_Template, Dir_With_Plugins
from . import BasePlugin


class PluginLoader:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)

        return cls.instance

    def __init__(self):
        self.__plugins: dict = {}

    @property
    def get(self) -> dict:
        return self.__plugins

    def load(self) -> None:
        plugin_template: str = Plugin_Template
        dir_with_plugins: str = Dir_With_Plugins
        path_to_plugins: str = self.__get_path(dir_with_plugins,
                                            plugin_template)

        for plugin in [file for file in glob(path_to_plugins)]:
            plugin_name: str = self.__get_full_name(plugin,
                                                 dir_with_plugins)
            self.__import(plugin_name)

        self.__initiate()

    def __import(self, plugin: str) -> None:
        try:
            import_module(plugin)
        except Exception as ex:
            print(f"Couldn't import plugin - {plugin} - {ex}")

    def __initiate(self) -> None:
        for plugin in BasePlugin.__subclasses__():
            if self.__is_correct_plugin(plugin):
                p: BasePlugin = plugin()
                self.__plugins.update({p.getName: p})

    def __is_correct_plugin(self, plugin: type[BasePlugin]) -> bool:
        return issubclass(plugin, BasePlugin)

    def __get_path(self, dirWithPlugin: str, nameTemplate: str) -> str:
        return path.abspath(
            path.realpath(path.dirname(__file__)
                + "/" + dirWithPlugin)) + nameTemplate

    def __get_full_name(self, plugin: str, dirWithPlugins: str) -> str:
        length_type_file: int = len('.py')

        plugin_name: str = path.basename(
            path.abspath(path.realpath(plugin)))[:-length_type_file]
        plugin_dir: str = path.basename(
            path.dirname(path.abspath(
                path.realpath(plugin))))
        path_to_local: str = path.basename(path.dirname(__file__))

        return (f"{path_to_local}"
                f".{dirWithPlugins}"
                f".{plugin_dir}"
                f".{plugin_name}")
