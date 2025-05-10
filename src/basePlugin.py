from abc import ABC, abstractmethod


class BasePlugin(ABC):
    @abstractmethod
    def getName(self):
        ...

    @abstractmethod
    def start(self):
        ...

    @abstractmethod
    def stop(self):
        ...
