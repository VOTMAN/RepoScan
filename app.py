from collections import deque

from extractors import extract
from graph import createGraph
from parsers.get_tree import get_tree
from repository.load import load_source
from storage.retreiver import ask_repo, rewrite_query
from storage.vec_db import getCollection


def app():
    repo_url = input("Enter a repository link: ")
    repo, trees = get_tree(repo_url)
    # repo, trees = get_tree("https://github.com/VOTMAN/passwordManager")

    repo_name = (repo.root.split("/")[-1]).lower()
    collection = getCollection(repo_name)

    for path, node in repo.files.items():
        source = load_source(path, repo.root)
        tree = trees.get(path)
        node = extract(node, tree, source)
        repo.files[path] = node

    if collection.count() == 0:
        for path, node in repo.files.items():
            print(f"=== {path} ===")
            ids = []
            documents = []
            metadatas = []
            for c in node.chunks:
                doc_id = f"{path}::{c.name}::{c.start_line}"
                ids.append(doc_id)
                documents.append(f"""
                    File: {c.path}
                    Type: {c.kind}
                    Name: {c.name}

                    Imports:
                    {", ".join(im.module for im in node.imports or [])}

                    Code:
                    {c.content}
                """)
                metadatas.append(
                    {
                        "name": c.name,
                        "kind": c.kind,
                        "path": c.path,
                        "start_line": c.start_line,
                        "end_line": c.end_line,
                        "exported": c.exported,
                        "language": c.language,
                    }
                )

            # print(ids, documents, metadatas, sep="\n\n")
            if not documents:
                continue

            collection.add(ids=ids, documents=documents, metadatas=metadatas)
    else:
        print("Repo already indexed. Continue")

    # G = createGraph(repo)

    history = []
    while True:
        qs = input("Enter your question: ")
        search_query = rewrite_query(qs)
        res = collection.query(query_texts=[search_query], n_results=5)
        # print(res)
        if qs.strip().lower() in ["q", "quit", "exit"]:
            print("Exiting...")
            return
        print("Please wait...")
        answer = ask_repo(repo_name, qs, str(history), n_results=5)
        print("LLM: \n")
        print(answer, end="\n\n")
        history.append({"User": qs, "Assistant": answer})


if __name__ == "__main__":
    app()
