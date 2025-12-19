import inspect
from typing import Sequence
from types import ModuleType

from ..interfaces.plugin import PluginBase
from ..interfaces.finder import PluginFinderBase


class PluginClassFinder(PluginFinderBase):
    def find(self, module: ModuleType) -> Sequence[str]:
        result = []

        for _, obj in inspect.getmembers(module, inspect.isclass):
            if (
                    issubclass(obj, PluginBase)
                    and obj is not PluginBase
                    and not inspect.isabstract(obj)
            ):
                result.append(obj)

        return result
