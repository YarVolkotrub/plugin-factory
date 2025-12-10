from abc import ABC, abstractmethod


class IFinderPlugin(ABC):
    @abstractmethod
    def get(self) -> list[str]:
        ...
