from __future__ import annotations

import logging
from typing import Type, TYPE_CHECKING

from plugin_factory.contracts import InstanceProtocol
from plugin_factory.core import PluginInfo
from plugin_factory.exceptions import PluginInstantiationError

if TYPE_CHECKING:
    from plugin_factory.core import PluginBase

logger = logging.getLogger(__name__)


class FactoryPlugin(InstanceProtocol):
    def get_instance(self, plugin_class: Type[PluginBase]) -> PluginBase:
        try:
            self.__validate_plugin_class(plugin_class)

            info = PluginInfo(
                name=plugin_class.NAME,
                description=plugin_class.DESCRIPTION,
            )

            return plugin_class(info)
        except TypeError as exc:
            raise PluginInstantiationError(
                "Failed to instantiate plugin '%s': '%s'"
                "invalid constructor signature",
                plugin_class.__name__, exc
            ) from exc
        except Exception as exc:
            raise PluginInstantiationError(
                "Failed to instantiate plugin '%s': '%s'",
                plugin_class.__name__, exc
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
            raise PluginInstantiationError(
                "Plugin DESCRIPTION must be string")
