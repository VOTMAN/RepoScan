from repository.load import load_source
from parsers.get_tree import get_tree
from extractors import extract
from storage.vec_db import getCollection
# from storage.LLM import questionAnswer
from storage.retreiver import ask_repo

repo, trees = get_tree("https://github.com/VOTMAN/SynciNote")
repo_name = repo.root.split("/")[-1]
collection = getCollection(repo_name)

for path, node in repo.files.items():
    ids = []
    documents = []
    metadatas = []

    source = load_source(path, repo.root)
    tree = trees.get(path)

    print(f"\n=== {path} ===")
    node = extract(node, tree, source)
    # print(node)

    
    for c in node.chunks:
        doc_id = f"{path}::{c.name}::{c.start_line}"
        ids.append(doc_id)
        documents.append(f"""
            File: {c.path}
            Type: {c.kind}
            Name: {c.name}

            Imports:
            {", ".join(node.imports or [])}

            Code:
            {c.content}
        """)
        metadatas.append({
            "name": c.name,
            "kind": c.kind,
            "path": c.path,
            "start_line": c.start_line,
            "end_line": c.end_line,
            "exported": c.exported,
            "language": c.language            
        })
        
    # print(ids, documents, metadatas, sep="\n\n")

    if not documents:
        continue

    collection.add(ids=ids, documents=documents, metadatas=metadatas)


qs = "How is the Markdown Editor Implemented"
# res = collection.query(query_texts=[qs], n_results=5)
# print(res)
ask_repo(repo_name, qs)