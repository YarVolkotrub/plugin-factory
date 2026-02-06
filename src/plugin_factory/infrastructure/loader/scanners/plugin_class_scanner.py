from __future__ import annotations

import inspect
import logging
from types import ModuleType
from typing import Type

from plugin_factory.contracts import ClassScannerProtocol
from plugin_factory.core import PluginBase
from plugin_factory.exceptions import PluginDefinitionError

logger = logging.getLogger(__name__)


class PluginClassScanner(ClassScannerProtocol):
    def get_class(self, module: ModuleType) -> Type[PluginBase]:
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if getattr(obj, '__module__', None) != module.__name__:
                continue

            if not (
                    issubclass(obj, PluginBase)
                    and obj is not PluginBase
                    and not inspect.isabstract(obj)
            ):
                raise PluginDefinitionError(
                    f"No PluginBase subclass found in module '%r'",
                    module.__name__
                )

            return obj


