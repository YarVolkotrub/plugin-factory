from __future__ import annotations

import logging
from typing import Type, TYPE_CHECKING

from plugin_factory.contracts import InstanceProtocol
from plugin_factory.exceptions import PluginInstantiationError
from plugin_factory.core import PluginInfo

if TYPE_CHECKING:
    from plugin_factory.core import PluginBase

logger = logging.getLogger(__name__)


class FactoryPlugin(InstanceProtocol):
    def get_instance(self, plugin_class: Type[PluginBase]) -> PluginBase:
        try:
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
