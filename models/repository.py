from dataclasses import dataclass

from .symbols import FileNode


@dataclass
class Repository:
    root: str
    name: str
    owner: str
    files: dict[str, FileNode]
