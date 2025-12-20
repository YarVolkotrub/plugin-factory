from __future__ import annotations
import logging
from types import ModuleType

from ..interfaces.plugin import PluginBase
from ..exceptions import PluginInstantiationError

logger = logging.getLogger(__name__)


class PluginFactory:
    def create(self, cls: ModuleType) -> PluginBase:
        try:
            logger.debug(f"Object '{ModuleType}' created - success")
            return cls()
        except Exception as exc:
            logger.error(f"Object '{ModuleType}' created - failed")
            raise PluginInstantiationError(cls.__name__) from exc
