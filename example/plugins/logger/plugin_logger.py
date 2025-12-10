from src import IPlugin


class LoggerPlugin(IPlugin):
    def __init__(self):
        self.__name = "Logger"

    @property
    def name(self) -> str:
        return self.__name

    @property
    def status(self) -> str:
        return "ready"

    def start(self) -> None:
        print("Logger started")

    def stop(self) -> None:
        print("Logger stopped")