from __future__ import annotations

import inspect
import logging
from types import ModuleType
from typing import Type

from plugin_factory.contracts import ClassScannerProtocol
from plugin_factory.core import PluginBase

logger = logging.getLogger(__name__)


class PluginClassScanner(ClassScannerProtocol):
    def get_class(self, module: ModuleType) -> Type[PluginBase] | None:
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if getattr(obj, '__module__', None) != module.__name__:
                continue

            if (
                    issubclass(obj, PluginBase)
                    and obj is not PluginBase
                    and not inspect.isabstract(obj)
            ):
                return obj
            else:
                logger.warning(
                    "Skipping class '%s'"
                    ": not a concrete PluginBase subclass",
                    obj.__name__
                )
        logger.warning(
            "No plugin class found in module: '%s'",
            module.__name__
        )
        return None
