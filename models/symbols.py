from dataclasses import dataclass

@dataclass
class FileNode:
    path: str
    language: str
    size: int
    extension: str

    imports: list[str] | None = None
    exports: list[str] | None = None

@dataclass
class FunctionNode:
    name: str
    infiles: list[str]
    path: str

@dataclass
class ClassNode:
    name:str
    infiles: list[str]
    path: str