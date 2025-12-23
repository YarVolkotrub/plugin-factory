import inspect
from typing import Sequence
from types import ModuleType
import logging

from ..interfaces.plugin import PluginBase
from ..interfaces.finder import PluginFinderBase

logger = logging.getLogger(__name__)


class PluginClassFinder:
    def get(self, module: ModuleType) -> ModuleType | None:
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
                logger.warning(f"Object '{obj}' is not a subclass of 'PluginBase'")

        return None
