import os
from dataclasses import dataclass
from git import Repo

EXTENSION_MAP = {
    "py": "python",
    "js": "javascript",
    "ts": "typescript",
    "svelte": "svelte",
    "go": "go",
    "rs": "rust",
    "java": "java",
    "cpp": "cpp",
    "c": "c",
    "css": "css",
    "html": "html",
    "md": "markdown",
    "json": "json",
    "yaml": "yaml",
    "toml": "toml",
}

IGNORE = {".git", "node_modules", "env", ".venv", "package-lock.json", "__pycache__", ".next"}

@dataclass
class FileNode:
    path: str
    language: str
    size: int
    extension: str

    imports: list[str] | None = None
    exports: list[str] | None = None

@dataclass
class Repository:
    root: str
    files: dict[str, FileNode]

def detect_language(filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1] if "." in filename else ""
    return EXTENSION_MAP.get(ext, "unknown")

def clone_repo(url: str) -> str:
    repo_name = url.split("/")[-1]
    local_dir = os.path.abspath(f"./repos/{repo_name}")

    if not os.path.exists(local_dir):
        Repo.clone_from(url, local_dir)
    else:
        print("Repo already exists")

    return local_dir

def load_repository(url: str) -> Repository:
    root = clone_repo(url)

    return Repository(
        root=root,
        files=build_struct(root),
    )

def build_struct(path: str, root: str | None = None) -> dict[str, FileNode]:
    result = {}
    if root is None:
        root = path


    for item in os.listdir(path):
        if item in IGNORE:
            continue

        abs_path = os.path.join(path, item)
        rel_path = os.path.relpath(abs_path, root)

        if os.path.isdir(abs_path):
            result.update(build_struct(abs_path, root))
        else:
            ext = item.rsplit(".", 1)[-1] if "." in item else ""
            result[rel_path] = FileNode(
                path=abs_path,
                language=detect_language(item),
                size=os.path.getsize(abs_path),
                extension=ext,
            )

    return result


def print_struct(result: dict[str, FileNode]) -> None:
    for path, node in result.items():
        print(f"{node.language:12} {node.size:6}B  {path}")