from src.Interfaces.IPlugin import IPlugin


class ExamplePlugin(IPlugin):
    def __init__(self):
        self.__name = "Example"
        self.__state = "stopped"

    @property
    def name(self) -> str:
        return self.__name

    @property
    def status(self) -> str:
        return self.__state

    def start(self) -> None:
        self.__state = "running"
        print("Example started")

    def stop(self) -> None:
        self.__state = "stopped"
        print("Example stopped")