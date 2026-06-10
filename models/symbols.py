from dataclasses import dataclass, field


@dataclass
class ChunkNode:
    name: str
    kind: str            # "function", "class", "interface", "type"
    path: str
    content: str
    start_line: int
    end_line: int
    exported: bool | str = False 
    language: str = ""

@dataclass
class ImportNode:
    module: str
    names: list[str]
    is_relative: bool

@dataclass
class FileNode:
    path: str
    language: str
    size: int
    extension: str

    imports: list[ImportNode] = field(default_factory=list)
    exports: list[str] = field(default_factory=list)
    chunks: list[ChunkNode] = field(default_factory=list)