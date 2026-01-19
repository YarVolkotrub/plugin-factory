from dataclasses import dataclass
from pathlib import Path


@dataclass
class FinderStorage:
    pattern: str
    path: Path
