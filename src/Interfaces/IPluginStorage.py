from abc import ABC, abstractmethod


class IPluginStorage(ABC):
    @property
    @abstractmethod
    def path(self) -> str:
        ...

    @abstractmethod
    def get(self) -> str:
        ...
