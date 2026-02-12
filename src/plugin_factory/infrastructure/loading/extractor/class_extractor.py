from __future__ import annotations

import inspect
from types import ModuleType
from typing import Type

from plugin_factory.interfaces import ClassExtractorProtocol
from plugin_factory.core import PluginBase
from plugin_factory.exceptions import PluginDefinitionError


class ClassExtractor(ClassExtractorProtocol):
    def extract_plugin_class(self, module: ModuleType) -> Type[PluginBase]:
        try:
            plugin_cls: Type[PluginBase] = module.__plugin__
        except AttributeError:
            raise PluginDefinitionError(
                f"Module '{module.__name__}' does not define __plugin__")

        if not issubclass(plugin_cls, PluginBase):
            raise PluginDefinitionError(
                "__plugin__ must be subclass of PluginBase")

        if inspect.isabstract(plugin_cls):
            raise PluginDefinitionError("Plugin class must be concrete")

        return plugin_cls

