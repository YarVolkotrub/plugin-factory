from __future__ import annotations
from typing import Type
from ..interfaces.plugin import PluginBase
from ..exceptions import PluginInstantiationError


class PluginFactory:
    def create(self, cls: Type[PluginBase]) -> PluginBase:
        try:
            return cls()
        except Exception as exc:
            raise PluginInstantiationError(cls.__name__) from exc
