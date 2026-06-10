from repository.load import load_repository, load_source
from repository.scanner import build_struct, print_struct
from parsers.get_tree import get_tree
from extractors import extract

# repo = load_repository(url="")

# struct = build_struct(repo.root)

# print_struct(struct)

repo, trees = get_tree("https://github.com/VOTMAN/SynciNote")

for path, node in repo.files.items():
    source = load_source(path, repo.root)

    tree = trees.get(path)

    if tree is None:
        continue

    node = extract(node, tree, source)
    print(f"\n=== {path} ===")
    print("imports:", node.imports)
    print("chunks:", [(c.name, c.kind, c.exported, c.content) for c in node.chunks])
