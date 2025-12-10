import logging
from ..Interfaces.IPlugin import IPlugin
from ..Interfaces.IPluginValidator import IPluginValidator

logger = logging.getLogger(__name__)


class PluginValidator(IPluginValidator):
    def is_valid(self, instance: IPlugin, plugins: dict[str, IPlugin]) -> bool:
        """
        Validate plugin instance: name correctness + duplicates.
        Returns True if plugin should be accepted.
        """
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
