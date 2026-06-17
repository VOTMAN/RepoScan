import os

import matplotlib.pyplot as plt
import networkx as nx
from networkx.classes.digraph import DiGraph

from models.repository import Repository


def createGraph(repo: Repository | None) -> DiGraph | None:
    if not repo:
        return

    G = nx.DiGraph()
    for _, node in repo.files.items():
        # print(node)
        # print()
        G.add_node(node.path)
        for im in node.imports or []:
            if not im.is_relative:
                continue

            resolved = resolve_import(node.path, im.module, repo)

            G.add_edge(node.path, resolved, imports=im.names)

    return G


def resolve_import(current_file: str, import_name: str, repo):
    base_dir = os.path.dirname(current_file)
    base = os.path.normpath(os.path.join(base_dir, import_name))

    candidates = [
        base,
        f"{base}.ts",
        f"{base}.tsx",
        f"{base}.js",
        f"{base}.jsx",
        f"{base}.py",
        f"{base}.svelte",
    ]

    for candidate in candidates:
        if candidate in repo.files:
            return candidate

    return base
