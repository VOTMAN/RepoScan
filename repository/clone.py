import os

from git import Repo

FILE_SIZE_LIMIT = "101m"
DEFAULT_FOLDER = "./repos"


def clone_repo(url: str) -> str:
    os.makedirs(DEFAULT_FOLDER, exist_ok=True)
    try:
        repo_name = (url.split("/")[-1]).lower()
        local_dir = os.path.abspath(f"./repos/{repo_name}")

        if not os.path.exists(local_dir):
            Repo.clone_from(
                url, local_dir, multi_options=[f"--filter=blob:limit={FILE_SIZE_LIMIT}"]
            )
        else:
            print("Repo already exists at clone_repo")
    except Exception as e:
        print(f"Error while cloning the repo: {e}")
        exit(1)
    return local_dir
