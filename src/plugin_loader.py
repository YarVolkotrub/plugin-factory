from __future__ import annotations

import inspect
import logging
import sys
from glob import glob
from importlib import import_module
from pathlib import Path

from typing import Final

from . import PLUGIN_TEMPLATE, PLUGIN_DIR_NAME
from .IPlugin import IPlugin
from .IPluginLoader import IPluginLoader

logger = logging.getLogger(__name__)


class PluginLoader(IPluginLoader):
    """Filesystem-based plugin loader.

    This implementation searches for files matching a glob pattern within a
    plugins directory, imports them as modules (by path) and instantiates
    concrete subclasses of :class:`IPlugin` defined in those modules.
    The loader returns a mapping of plugin names to plugin instances.
    """

    def __init__(
        self,
        plugin_template: str = PLUGIN_TEMPLATE,
        dir_with_plugins: str = PLUGIN_DIR_NAME
    ) -> None:
        if (
                not isinstance(plugin_template, str)
                or not isinstance(dir_with_plugins, str)
        ):
            raise TypeError(
                "plugin_template and dir_with_plugins must be strings"
            )

        self.__plugin_template: Final[str] = plugin_template
        self.__dir_with_plugins: Final[str] = dir_with_plugins
        self.__plugins: dict[str, IPlugin] = {}
        self.__imported_modules: list[str] = []

    @property
    def plugins(self) -> dict[str, IPlugin]:
        """Return a shallow copy of loaded plugins."""
        return dict(self.__plugins)

    def load(self) -> dict[str, IPlugin]:
        """Load plugins from filesystem and return {name: instance} dict."""
        path_to_plugins: str = self.__get_path(
            self.__dir_with_plugins, self.__plugin_template
        )

        for plugin in glob(path_to_plugins):
            plugin_name: str = self.__get_full_name(plugin,
                                                    self.__dir_with_plugins)
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
        """Discover, validate and instantiate plugin classes."""
        for module_name in list(self.__imported_modules):
            module = sys.modules.get(module_name)

            if module is None:
                continue

            classes = self.__discover_plugin_classes(module, module_name)
            for cls in classes:
                instance = self.__instantiate_plugin(cls)
                if instance is None:
                    continue

                if not self.__validate_plugin(instance):
                    continue

                self.__plugins[instance.name] = instance

    def __instantiate_plugin(self, cls: type[IPlugin]) -> IPlugin | None:
        """Instantiate plugin class, return None if failed."""
        try:
            return cls()
        except Exception:
            logger.exception(
                "Failed to instantiate plugin class %s", cls.__name__
            )
            return None

    def __validate_plugin(self, instance: IPlugin) -> bool:
        """
        Validate plugin instance: name correctness + duplicates.
        Returns True if plugin should be accepted.
        """
        name = getattr(instance, "name", None)

        if not isinstance(name, str) or not name:
            logger.warning(
                "Plugin %s returned invalid name: %r",
                instance.__class__.__name__,
                name
            )
            return False

        if name in self.__plugins:
            logger.warning("Duplicate plugin name %s; skipping", name)
            return False

        return True

    def __discover_plugin_classes(
            self,
            module,
            module_name: str
    ) -> list[type[IPlugin]]:
        """Return list of concrete IPlugin subclasses defined in the module."""
        discovered = []

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

            discovered.append(obj)

        return discovered

    def __get_path(self, dir_with_plugin: str, name_template: str) -> str:
        base_dir = Path(__file__).resolve().parent
        suffix = name_template.lstrip("/\\")
        base_plugins_dir = (base_dir / dir_with_plugin).resolve()

        if base_dir not in base_plugins_dir.parents:
            raise ValueError(
                f"Plugins directory must be inside {base_dir}, "
                f"got {base_plugins_dir}"
            )

        return str(base_plugins_dir / suffix)

    def __get_full_name(self, plugin: str, dir_with_plugins: str) -> str:
        path_obj = Path(plugin).resolve()
        plugin_name = path_obj.stem
        plugin_dir = path_obj.parent.name
        package_name = Path(__file__).resolve().parent.name

        return f"{package_name}.{dir_with_plugins}.{plugin_dir}.{plugin_name}"
