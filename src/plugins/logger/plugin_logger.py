from src.IPlugin import IPlugin


class LoggerPlugin(IPlugin):
    def __init__(self):
        self.__name = "Logger"
        self.__state = str()

    @property
    def name(self) -> str:
        return self.__name

    @property
    def status(self) -> str:
        return self.__state

    def start(self) -> None:
        self.__state = "run"
        print("Logger started")

    def stop(self) -> None:
        self.__state = "stop"
        print("Logger stopped")