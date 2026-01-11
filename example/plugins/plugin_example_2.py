from plugin_factory import PluginBase
from plugin_factory import PluginInfo


class ExamplePlugin2(PluginBase):
    """Test plugin 2"""

    def __init__(self):
        self.__info: PluginInfo = PluginInfo(
            name="Example",  # Уникальное имя плагина
            description="Test plugin is duplicate name."
        )

    @property
    def info(self) -> PluginInfo:
        return self.__info

    @info.setter
    def info(self, value: PluginInfo) -> None:
        self.__info = value

    def initialize(self) -> None:
        ...

    def start(self) -> None:
        ...

    def shutdown(self) -> None:
        ...