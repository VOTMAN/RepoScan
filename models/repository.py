from dataclasses import dataclass
from .symbols import FileNode

@dataclass
class Repository:
    root: str
    files: dict[str, FileNode]