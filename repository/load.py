import os

from models.repository import Repository

from .scanner import build_struct
# from clone import clone_repo

def load_repository(url: str) -> Repository:
    # root = clone_repo(url)

    # return Repository(
    #     root=root,
    #     files=build_struct(root),
    # )

    return Repository(
        root=os.path.abspath("./repos/test"),
        files=build_struct(os.path.abspath("./repos/test"))
    )