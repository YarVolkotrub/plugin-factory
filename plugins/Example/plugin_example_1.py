from src.interfaces.plugin import PluginBase
from src.interfaces.plugin import InfoBase


class ExamplePlugin1(PluginBase):
    """Test plugin is not a subclass of 'PluginBase'"""

    def __init__(self):
        self.__name = "Example"

    @property
    def name(self) -> str:
        return self.__name

    @property
    def info(self) -> type[InfoBase]:
        return InfoBase

    def init(self) -> None:
        ...

    def start(self) -> None:
        ...
