from src.interfaces.plugin import PluginBase
from src.dataclasses.info import InfoBase

class TestPlugin(PluginBase):
    def __init__(self):
        self.__name = "Example"
        self.__state = "stopped"

    @property
    def name(self) -> str:
        return self.__name

    @property
    def info(self) -> InfoBase:
        return InfoBase(name=self.__name, state=self.__state)

    def init(self) -> None:
        ...

    def start(self) -> None:
        self.__state = "running"
        print("Example started")

    def stop(self) -> None:
        self.__state = "stopped"
        print("Example stopped")
