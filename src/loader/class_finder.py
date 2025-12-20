import inspect
from typing import Sequence
from types import ModuleType
import logging

from ..interfaces.plugin import PluginBase
from ..interfaces.finder import PluginFinderBase

logger = logging.getLogger(__name__)


class PluginClassFinder(PluginFinderBase):
    def find(self, module: ModuleType) -> Sequence[ModuleType]:
        result = []

        for _, obj in inspect.getmembers(module, inspect.isclass):
            if (
                    issubclass(obj, PluginBase)
                    and obj is not PluginBase
                    and not inspect.isabstract(obj)
            ):
                result.append(obj)
                logger.debug(f"Plugin '{obj.__name__}' found - {obj}")
            else:
                logger.warning(f"Object '{obj}' is not a subclass of 'PluginBase'")

        return result
