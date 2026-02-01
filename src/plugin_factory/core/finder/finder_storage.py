from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class FinderStorage:
    pattern: str
    path: Path
