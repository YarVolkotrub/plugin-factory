import logging
from src.interfaces.plugin import PluginBase
from src.interfaces.validator import PluginValidatorBase

logger = logging.getLogger(__name__)


class PluginValidator(PluginValidatorBase):
    """
    This validator checks structural plugin contract only.
    It does not validate lifecycle order or runtime state.
    """
    def is_valid(self, instance: PluginBase, plugins: dict[str, PluginBase]) -> bool:
        try:
            name = instance.name
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

        if name in plugins:
            logger.warning("Duplicate plugin %s", name)
            return False
        return True
