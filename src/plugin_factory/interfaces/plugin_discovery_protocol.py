from abc import abstractmethod
from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from plugin_factory.core import FinderStorage


class PluginDiscoveryProtocol(Protocol):
    @abstractmethod
    def find_in_directory(self, storage: FinderStorage) -> None: ...
