from src.domain.plugin import PluginBase
from src.domain.plugin import PluginInfo


class ExamplePlugin0(PluginBase):
    """Test plugin 0"""

    def __init__(self):
        self.__info: PluginInfo = PluginInfo(
            name="Example0",  # Уникальное имя плагина
            description="Example plugin for demonstration."
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
