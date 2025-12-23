import logging
from src.domain.plugin import PluginBase
from src.interfaces.validator import PluginValidatorBase

logger = logging.getLogger(__name__)


class StructuralPluginValidator(PluginValidatorBase):
    """
    This validator checks structural plugin contract only.
    It does not validate lifecycle order or runtime state.
    """
    def is_valid(self, plugin: PluginBase, existing_plugins: dict[str, PluginBase]) -> bool:
        try:
            name = plugin.name
        except AttributeError:
            logger.warning("Plugin missing 'name' attribute: %s", type(plugin).__name__)
            return False

        if not isinstance(name, str):
            logger.warning("Plugin name must be string, got %s: %s",
                          type(name).__name__, repr(name))
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
