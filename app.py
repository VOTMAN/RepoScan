from repository.load import load_repository
from repository.scanner import build_struct, print_struct
from parsers.get_tree import get_tree

repo = load_repository(url="")

struct = build_struct(repo.root)

print_struct(struct)

trees = get_tree()

print(trees)