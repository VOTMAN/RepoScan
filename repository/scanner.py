import os

from models.symbols import FileNode

EXTENSION_MAP = {
    "py": "python",
    "js": "javascript",
    "ts": "typescript",
    "jsx": "javascript xml",
    "tsx": "typescript xml",
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

SUPPORTED_EXTENSIONS = {
    "py",
    "js",
    "ts",
    "tsx",
    "jsx",
    "svelte",
    "css",
    "html",
    "json",
    "yaml",
    "yml",
    "toml",
    "md",
}

IGNORE = {
    ".git",
    "node_modules",
    "env",
    ".venv",
    "package-lock.json",
    "__pycache__",
    ".next",
    "README.md",
}


def detect_language(filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1] if "." in filename else ""
    return EXTENSION_MAP.get(ext, "unknown")


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

            if ext not in SUPPORTED_EXTENSIONS:
                continue

            result[rel_path] = FileNode(
                path=rel_path,
                language=detect_language(item),
                size=os.path.getsize(abs_path),
                extension=ext,
            )

    return result


def print_struct(result: dict[str, FileNode]) -> None:
    for path, node in result.items():
        print(f"{node.language:12} {node.size:6}B  {path}")
