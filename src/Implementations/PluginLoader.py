from __future__ import annotations

import inspect
import logging
import sys
from importlib import import_module

from types import ModuleType, MappingProxyType

from ..Interfaces.IPlugin import IPlugin
from ..Interfaces.IPluginLoader import IPluginLoader
from ..Interfaces.IPluginValidator import IPluginValidator
from ..Interfaces.IFinderPlugin import IFinderPlugin

logger = logging.getLogger(__name__)


class PluginLoader(IPluginLoader):
    def __init__(
        self,
        finder_plugin: IFinderPlugin,
        plugin_validator: IPluginValidator
    ) -> None:
        self.__finder_plugin: IFinderPlugin = finder_plugin
        self.__plugin_validator: IPluginValidator = plugin_validator
        self.__plugins: dict[str, IPlugin] = {}
        self.__imported_modules: list[str] = []

    @property
    def plugins(self) -> MappingProxyType[str, IPlugin]:
        return MappingProxyType(self.__plugins)

    def load(self) -> MappingProxyType[str, IPlugin]:
        path_to_plugins: list[str] = self.__finder_plugin.get()

        for plugin_name in path_to_plugins:
            self.__import_module(plugin_name)

        self.__initiate()

        return self.plugins

    def __import_module(self, plugin: str) -> None:
        try:
            import_module(plugin)
            self.__imported_modules.append(plugin)
        except ImportError as ex:
            logger.error("Failed to import plugin %s: %s", plugin, ex)
        except SyntaxError as ex:
            logger.error("Syntax error in plugin %s: %s", plugin, ex)

    def __initiate(self) -> None:
        for module_name in list(self.__imported_modules):
            module = sys.modules.get(module_name)

            if module is None:
                continue

            classes = self.__discover_plugin_classes(module, module_name)

            for cls in classes:
                instance = self.__instantiate_plugin(cls)
                if instance is None:
                    continue

                if not self.__plugin_validator.is_valid(
                    instance,
                    dict(self.__plugins)
                ):
                    continue

                self.__plugins[instance.name] = instance

    def __instantiate_plugin(self, cls: type[IPlugin]) -> IPlugin | None:
        try:
            return cls()
        except Exception:
            logger.exception(
                "Failed to instantiate plugin class %s", cls.__name__
            )
            return None

    def __discover_plugin_classes(
            self,
            module: ModuleType,
            module_name: str
    ) -> list[type[IPlugin]]:
        discovered = []

        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, IPlugin) and obj is not IPlugin:
                if not inspect.isabstract(obj):
                    discovered.append(obj)

        return discovered
