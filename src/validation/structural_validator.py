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
            logger.warning("Plugin missing 'name' attribute")
            return False

        if not isinstance(name, str):
            logger.warning("Plugin name must be string")
            return False

        name = name.strip()
        if not name:
            logger.warning("Plugin name cannot be empty")
            return False

        if name in existing_plugins:
            logger.warning("Duplicate plugin %s", name)
            return False
        return True
