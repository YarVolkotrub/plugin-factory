from abc import abstractmethod
from pathlib import Path
from typing import Protocol


class FinderPath(Protocol):
    @abstractmethod
    def find_in_directories(
            self,
            directories: list[Path],
            pattern: str
    ) -> None: ...
