import os

import networkx as nx
from networkx.classes.digraph import DiGraph

from models.repository import Repository


def createGraph(repo: Repository | None) -> DiGraph | None:
    if not repo:
        return None

    G = nx.DiGraph()

    for _, node in repo.files.items():
        G.add_node(node.path)

    for _, node in repo.files.items():
        for im in node.imports or []:
            target = resolve_import(
                current_file=node.path,
                import_name=im.module,
                repo=repo,
            )

            if target and target in repo.files:
                G.add_edge(
                    target,
                    node.path,
                    imports=im.names,
                )

    return G


def resolve_import(
    current_file: str,
    import_name: str,
    repo: Repository,
) -> str | None:

    if import_name.startswith("."):
        base_dir = os.path.dirname(current_file)
        base = os.path.normpath(os.path.join(base_dir, import_name))

        candidates = [
            base,
            f"{base}.ts",
            f"{base}.tsx",
            f"{base}.js",
            f"{base}.jsx",
            f"{base}.svelte",
            f"{base}.py",
        ]

        for candidate in candidates:
            if candidate in repo.files:
                return candidate

        return None

    # Python imports
    dotted = import_name.replace(".", "/")

    candidates = [
        f"{dotted}.py",
        f"{dotted}/__init__.py",
    ]

    for candidate in candidates:
        if candidate in repo.files:
            return candidate

    # Bare module imports

    basename = f"{import_name}.py"

    matches = [path for path in repo.files if path.endswith(basename)]

    if len(matches) == 1:
        return matches[0]

    return None
