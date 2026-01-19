from abc import abstractmethod
from typing import Protocol, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from plugin_factory.core import PluginBase


class InstanceProtocol(Protocol):
    @abstractmethod
    def get_instance(self, plugin_class: Type[PluginBase]) -> PluginBase: ...
