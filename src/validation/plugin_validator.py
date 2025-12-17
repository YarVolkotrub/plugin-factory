import logging
from src.interfaces.plugin import PluginBase
from src.interfaces.validator import PluginValidatorBase

logger = logging.getLogger(__name__)


class PluginValidator(PluginValidatorBase):
    def is_valid(self, instance: PluginBase, plugins: dict[str, PluginBase]) -> bool:
        name = getattr(instance, "name", None)

        if not isinstance(name, str) or not name:
            logger.warning(
                "Plugin %s returned invalid name: %r",
                instance.__class__.__name__,
                name
            )
            return False

        if name in plugins:
            logger.warning("Duplicate plugin name %s; skipping", name)
            return False
        return True
