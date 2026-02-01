from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Dict

from plugin_factory.contracts import PluginValidatorProtocol

if TYPE_CHECKING:
    from plugin_factory.core import PluginBase

logger = logging.getLogger(__name__)


class StructuralPluginValidator(PluginValidatorProtocol):
    def is_valid(
            self,
            plugin: PluginBase,
            existing_plugins: Dict[str, PluginBase]
    ) -> bool:
        try:
            name = plugin.info.name
        except AttributeError:
            logger.warning(
                "Plugin missing 'name' attribute: '%s'",
                type(plugin).__name__
            )
            return False

        if not isinstance(name, str):
            logger.warning(
                "Plugin name must be string, got '%s': '%s'",
                type(name).__name__, repr(name)
            )
            return False

        name = name.strip()

        if not name:
            logger.warning("Plugin name cannot be empty or whitespace only")
            return False

        if name in existing_plugins:
            logger.warning("Duplicate plugin name: '%s'", name)
            return False

        logger.debug("Plugin validation passed: '%s'", name)
        return True
