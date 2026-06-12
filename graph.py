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

            resolved = resolve_import(node.path, im.module)
            G.add_edge(node.path, resolved)

    pos = nx.spring_layout(G, seed=68)
    plt.figure(figsize=[20, 20])
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=500,
        node_color="skyblue",
    )
    plt.title("Dependency Graph")
    plt.savefig("graph.png")

    return G


def resolve_import(current_file: str, import_name: str):
    base_dir = os.path.dirname(current_file)
    base = os.path.normpath(os.path.join(base_dir, import_name))

    for ext in ["ts", "tsx", "js", "jsx", "py"]:
        candidate = f"{base}.{ext}"
        if os.path.exists(candidate):
            return candidate

    return base
