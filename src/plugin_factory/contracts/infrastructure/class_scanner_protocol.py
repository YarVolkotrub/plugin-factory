from abc import abstractmethod
from types import ModuleType
from typing import Type, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from plugin_factory.core import PluginBase


class ClassScannerProtocol(Protocol):
    @abstractmethod
    def get_class(self, module: ModuleType) -> Type[PluginBase]: ...
