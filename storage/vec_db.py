import chromadb
import chromadb.utils.embedding_functions as ef
chroma_client = chromadb.PersistentClient(path="./chroma_db")


ollama_ef = ef.OllamaEmbeddingFunction(
    model_name="nomic-embed-text", 
    url="http://localhost:11434/api/embeddings"    
)

def getCollection(repo_name: str):
    return chroma_client.get_or_create_collection(
        name=repo_name,
        embedding_function=ollama_ef,
        configuration={
            "hnsw": {
                "space": "cosine"
            }
        }
    )