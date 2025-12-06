from glob import glob
from importlib import import_module
from pathlib import Path
import logging
import sys
import inspect

from . import PLUGIN_TEMPLATE, PLUGIN_DIR_NAME
from .IPlugin import IPlugin


class PluginLoader:
    def __init__(self, plugin_template: str = PLUGIN_TEMPLATE,
                 dir_with_plugins: str = PLUGIN_DIR_NAME):
        if not isinstance(plugin_template, str) or not isinstance(
                dir_with_plugins, str):
            raise TypeError("attribute is not correct")

        self.__plugin_template: str = plugin_template
        self.__dir_with_plugins: str = dir_with_plugins
        self.__plugins: dict[str, IPlugin] = {}
        self.__imported_modules: list[str] = []

    @property
    def plugins(self) -> dict[str, IPlugin]:
        return dict(self.__plugins)

    def load(self) -> dict[str, IPlugin]:
        path_to_plugins: str = self.__get_path(self.__dir_with_plugins,
                                               self.__plugin_template)

        for plugin in [file for file in glob(path_to_plugins)]:
            plugin_name: str = self.__get_full_name(plugin,
                                                    self.__dir_with_plugins)
            self.__import_module(plugin_name)

        self.__initiate()

        return self.plugins

    def __import_module(self, plugin: str) -> None:
        try:
            import_module(plugin)
            self.__imported_modules.append(plugin)
        except Exception as ex:
            logging.error("Failed to import plugin %s: %s", plugin, ex)

    def __initiate(self) -> None:
        for module_name in list(self.__imported_modules):
            module = sys.modules.get(module_name)

            if module is None:
                continue

            for attr in dir(module):
                obj = getattr(module, attr)

                if not isinstance(obj, type):
                    continue

                if not issubclass(obj, IPlugin) or obj is IPlugin:
                    continue

                if getattr(obj, "__module__", None) != module_name:
                    continue

                if inspect.isabstract(obj):
                    continue
                try:
                    instance: IPlugin = obj()
                except Exception:
                    logging.exception("Failed to instantiate plugin class %s",
                                      obj)
                    continue

                name = getattr(instance, "name", None)

                if not isinstance(name, str) or not name:
                    logging.warning("Plugin %s returned invalid name: %r", obj,
                                    name)
                    continue

                if name in self.__plugins:
                    logging.warning("Duplicate plugin name %s; skipping", name)
                    continue

                self.__plugins[name] = instance

    def __get_path(self, dir_with_plugin: str, name_template: str) -> str:
        base_dir = Path(__file__).resolve().parent
        suffix = name_template.lstrip("/\\")
        base_plugins_dir = (base_dir / dir_with_plugin).resolve()

        return str(base_plugins_dir / suffix)

    def __get_full_name(self, plugin: str, dir_with_plugins: str) -> str:
        path_obj = Path(plugin).resolve()
        plugin_name = path_obj.stem
        plugin_dir = path_obj.parent.name
        package_name = Path(__file__).resolve().parent.name

        return f"{package_name}.{dir_with_plugins}.{plugin_dir}.{plugin_name}"
