from .vec_db import getCollection
from .LLM import questionAnswer


def ask_repo(repo_name: str, question: str, n_results: int = 5):

    if not repo_name or not question:
        print("Fill all fields")
        return
    
    collection = getCollection(repo_name)
    count = collection.count()
    n_results = min(n_results, count)

    res = collection.query(query_texts=[question], n_results=n_results)

    documents = res["documents"][0]

    context = "\n\n".join(documents)

    answer = questionAnswer(context, question)
    print(answer)
    return answer