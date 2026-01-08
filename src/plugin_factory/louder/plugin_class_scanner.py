from __future__ import annotations

import inspect
import logging

from types import ModuleType
from typing import Type

from plugin_factory.domain import PluginBase

logger = logging.getLogger(__name__)


class PluginClassScanner:
    def get_class(self, module: ModuleType) -> Type[PluginBase] | None:
        logger.debug("Scanning for plugin class in module: %s", module.__name__)

        for _, obj in inspect.getmembers(module, inspect.isclass):
            if getattr(obj, '__module__', None) != module.__name__:
                continue

            if (
                    issubclass(obj, PluginBase)
                    and obj is not PluginBase
                    and not inspect.isabstract(obj)
            ):
                logger.info("Found plugin class '%s' in module '%s'",
                           obj.__name__, module.__name__)
                return obj
            else:
                logger.debug("Skipping class '%s': not a concrete PluginBase subclass",
                            obj.__name__)
        logger.debug("No plugin class found in module: %s", module.__name__)
        return None
