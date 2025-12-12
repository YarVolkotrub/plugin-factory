from pathlib import Path
from glob import glob

from ..Interfaces.IFinderPlugin import IFinderPlugin
from ..Interfaces.IPluginStorage import IPluginStorage


class FinderLocalPlugin(IFinderPlugin):
    def __init__(self, storage: IPluginStorage):
        self.__storage: IPluginStorage = storage

    def get(self) -> list[str]:
        path_pattern: str = self.__storage.get()
        plugins: list[str] = []

        for plugin_path in glob(path_pattern, recursive=True):
            plugin_name: str = self.__get_full_name(plugin_path)
            plugins.append(plugin_name)

        return plugins

    def __get_full_name(self, plugin_path: str) -> str:
        file_path = Path(plugin_path).resolve()
        project_root = Path(__file__).resolve().parent.parent.parent

        try:
            rel = file_path.relative_to(project_root)
            rel_no_ext = rel.with_suffix("")

            return ".".join(rel_no_ext.parts)

        except ValueError:
            return ".".join(file_path.parts[-3:]).replace(".py", "")