from __future__ import annotations

from abc import ABC, abstractmethod

from ..data.plugin_info import PluginInfo


class PluginBase(ABC):
    """
    Базовый контракт плагина.

    Менеджер НИКОГДА не вызывает ничего,
    кроме этих методов.
    """

    info: PluginInfo

    @abstractmethod
    def init(self) -> None:
        """
        Подготовка плагина.
        Повторный вызов допускается только после STOP.
        """
        raise NotImplementedError

    @abstractmethod
    def start(self) -> None:
        """
        Запуск основной логики плагина.
        """
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        """
        Остановка и освобождение ресурсов.
        """
        raise NotImplementedError
