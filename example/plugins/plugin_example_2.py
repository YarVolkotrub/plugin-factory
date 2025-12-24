from src.domain.plugin import PluginBase
from src.domain.plugin import PluginInfo


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

    def init(self) -> None:
        ...

    def start(self) -> None:
        ...

    def stop(self) -> None:
        ...