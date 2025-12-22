from src.interfaces.plugin import PluginBase
from src.interfaces.plugin import PluginInfo


class ExamplePlugin2(PluginBase):
    """Test plugin duplicate of 'ExamplePlugin2'."""

    def __init__(self):
        self.__name = "Example2"

    @property
    def name(self) -> str:
        return self.__name

    @property
    def info(self) -> type[PluginInfo]:
        return PluginInfo

    def init(self) -> None:
        ...

    def start(self) -> None:
        ...

    def stop(self) -> None:
        ...