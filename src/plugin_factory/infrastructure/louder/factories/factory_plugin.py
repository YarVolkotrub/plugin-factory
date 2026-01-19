from __future__ import annotations

import logging
from typing import Type, TYPE_CHECKING

from plugin_factory.contracts import InstanceProtocol
from plugin_factory.exceptions.exceptions import PluginInstantiationError

if TYPE_CHECKING:
    from plugin_factory.core import PluginBase

logger = logging.getLogger(__name__)


class FactoryPlugin(InstanceProtocol):
    def get_instance(self, plugin_class: Type[PluginBase]) -> PluginBase:
        try:
            return plugin_class()
        except TypeError as exc:
            raise PluginInstantiationError(
                "Failed to instantiate plugin '%s': %s"
                "invalid constructor signature",
                plugin_class.__name__, exc
            ) from exc
        except Exception as exc:
            raise PluginInstantiationError(
                "Failed to instantiate plugin '%s': %s",
                plugin_class.__name__, exc
            ) from exc
