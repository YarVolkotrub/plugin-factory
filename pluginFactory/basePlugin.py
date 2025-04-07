from abc import ABC, abstractmethod, abstractproperty


class BasePlugin(ABC):
    @abstractproperty
    def getName(self):
        ...

    @abstractmethod
    def run(self):
        ...

    @abstractmethod
    def stop(self):
        ...
