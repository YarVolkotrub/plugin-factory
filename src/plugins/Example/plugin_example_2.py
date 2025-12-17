from src.interfaces.plugin import PluginBase
from src.interfaces.plugin import InfoBase


class ExamplePluginBase(PluginBase):
    def __init__(self):
        self.__name = "Example2"
        self.__state = "stopped"

    @property
    def name(self) -> str:
        return self.__name

    @property
    def info(self) -> InfoBase:
        return InfoBase(name=self.__name, state=self.__state)

    def start(self) -> None:
        self.__state = "running"
        print("Example started")

    def stop(self) -> None:
        self.__state = "stopped"
        print("Example stopped")