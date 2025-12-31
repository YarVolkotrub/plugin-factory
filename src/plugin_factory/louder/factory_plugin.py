from __future__ import annotations

import logging

from typing import Type, TYPE_CHECKING

from plugin_factory.exceptions.exceptions import PluginInstantiationError

if TYPE_CHECKING:
    from plugin_factory.domain.plugin_base import PluginBase

logger = logging.getLogger(__name__)


class FactoryPlugin:
    def create(self, plugin_class: Type[PluginBase]) -> PluginBase:
        logger.debug("Instantiating plugin: %s", plugin_class.__name__)
        try:
            logger.info("Successfully instantiated plugin: %s", plugin_class.__name__)

            return plugin_class()
        except Exception as exc:
            logger.error("Failed to instantiate plugin '%s': %s",
                        plugin_class.__name__, exc)
            raise PluginInstantiationError(plugin_class.__name__) from exc
