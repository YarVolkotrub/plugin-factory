from abc import abstractmethod
from pathlib import Path
from typing import Protocol


class FinderPathProtocol(Protocol):
    @abstractmethod
    def find_in_directory(
            self,
            plugin_dir: Path,
            pattern: str
    ) -> None: ...
