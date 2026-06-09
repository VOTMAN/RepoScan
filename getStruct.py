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

def build_struct(path: str) -> dict[str, FileNode]:
    result = {}

    for item in os.listdir(path):
        if item in IGNORE:
            continue

        abs_path = os.path.join(path, item)
        rel_path = os.path.relpath(abs_path)

        if os.path.isdir(abs_path):
            result.update(build_struct(abs_path))
        else:
            result[rel_path] = FileNode(
                path=rel_path,
                language=detect_language(item),
                size=os.path.getsize(abs_path),
            )

    return result


local_dir = clone_repo("https://github.com/VOTMAN/SynciNote")
struct = build_struct(local_dir)

for path, node in struct.items():
    print(f"{node.language:12} {node.size:6}B  {path}")