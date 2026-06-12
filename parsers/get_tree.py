import os

from repository.load import load_repository

from .parser_registry import get_parser


def get_tree(repo_url: str | None = None):
    trees = {}
    if repo_url is None:
        print("No repo link given")
        return

    repo = load_repository(repo_url)

    for rel_path, node in repo.files.items():
        parser = get_parser(node.extension)

        if parser is None:
            continue

        abs_path = os.path.join(repo.root, node.path)
        try:
            with open(abs_path, "r", encoding="utf-8") as f:
                code = f.read()

            tree = parser.parse(code.encode("utf-8"))
            trees[rel_path] = tree
        except Exception as e:
            print(f"Failed to parse: {rel_path}")
            print(e)

    return repo, trees
