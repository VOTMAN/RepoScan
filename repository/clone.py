import os
from git import Repo

def clone_repo(url: str) -> str:
    repo_name = url.split("/")[-1]
    local_dir = os.path.abspath(f"./repos/{repo_name}")

    if not os.path.exists(local_dir):
        Repo.clone_from(url, local_dir)
    else:
        print("Repo already exists")

    return local_dir