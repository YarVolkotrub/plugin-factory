from src.interfaces.plugin import PluginBase
from src.interfaces.plugin import InfoBase


class ExamplePlugin0(PluginBase):
    """Test plugin 0"""

    def __init__(self):
        self.__name = "Example0"

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