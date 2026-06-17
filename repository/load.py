import os

from models.repository import Repository

from .clone import clone_repo
from .scanner import build_struct


def load_repository(url: str) -> Repository:
    root, name, owner = clone_repo(url)

    return Repository(
        root=root,
        name=name,
        owner=owner,
        files=build_struct(path=root),
    )

    # return Repository(
    #     root=os.path.abspath("./repos/test"),
    #     files=build_struct(os.path.abspath("./repos/test"))
    # )


def load_source(path: str, root: str):
    rel_path = os.path.abspath(os.path.join(root, path))
    with open(rel_path, "r", encoding="utf-8") as f:
        source = f.read()

    return source
