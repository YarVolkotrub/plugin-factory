from pathlib import Path

from ..Interfaces.IPluginStorage import IPluginStorage

PLUGIN_TEMPLATE: str = '/*/plugin*.py'
PLUGIN_DIR_NAME: str = str(Path(__file__).parent.parent.parent / 'plugins')


class LocalStorage(IPluginStorage):
    def __init__(
        self,
        template: str = PLUGIN_TEMPLATE,
        dir_with_template: str = PLUGIN_DIR_NAME
    ):
        self.__template: str = template
        self.__plugin_dir: str = dir_with_template

    @property
    def path(self) -> str:
        return str(self.__plugin_dir)

    def get(self) -> str:
        plugin_dir = Path(self.__plugin_dir).resolve()

        if not plugin_dir.exists():
            raise ValueError(f"Plugins directory does not exist: {plugin_dir}")

        pattern = self.__template.lstrip("/\\")

        return str(plugin_dir / pattern)
