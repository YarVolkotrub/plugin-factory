from src.interfaces.plugin import PluginBase
from src.interfaces.plugin import InfoBase


class ExamplePlugin1(PluginBase):
    """Test plugin 1"""

    def __init__(self):
        self.__name = "Example1"

    @property
    def name(self) -> str:
        return self.__name

    @property
    def info(self) -> type[InfoBase]:
        return InfoBase

    def init(self) -> None:
        print(f"Example init {self.__name}")

    def start(self) -> None:
        print(f"Example started {self.__name}")

    def stop(self) -> None:
        print(f"Example stopped {self.__name}")