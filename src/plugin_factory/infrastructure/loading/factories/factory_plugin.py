from __future__ import annotations

from typing import Type, TYPE_CHECKING

from plugin_factory.interfaces import PluginInstanceProtocol
from plugin_factory.core import PluginMetadata
from plugin_factory.exceptions import PluginInstantiationError

if TYPE_CHECKING:
    from plugin_factory.core import PluginBase


class PluginInstanceFactory(PluginInstanceProtocol):
    def get_instance(self, plugin_class: Type[PluginBase]) -> PluginBase:
        try:
            self.__validate_plugin_class(plugin_class)

            info = PluginMetadata(
                name=plugin_class.NAME,
                description=plugin_class.DESCRIPTION,
            )

            return plugin_class(info)
        except TypeError as exc:
            raise PluginInstantiationError(
                f"Failed to instantiate plugin "
                f"'{plugin_class.__name__}': '{exc}'"
                "invalid constructor signature"
            ) from exc
        except Exception as exc:
            raise PluginInstantiationError(
                f"Failed to instantiate plugin "
                f"'{plugin_class.__name__}': '{exc}'"
            ) from exc

    def __validate_plugin_class(self, plugin_class: Type[PluginBase]) -> None:
        if not hasattr(plugin_class, "NAME"):
            raise PluginInstantiationError("Plugin must define NAME")

        if not isinstance(plugin_class.NAME,
                          str) or not plugin_class.NAME.strip():
            raise PluginInstantiationError(
                "Plugin NAME must be non-empty string")

        if not hasattr(plugin_class, "DESCRIPTION"):
            raise PluginInstantiationError("Plugin must define DESCRIPTION")

        if not isinstance(plugin_class.DESCRIPTION, str):
            raise PluginInstantiationError("Plugin DESCRIPTION must be string")
