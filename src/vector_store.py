import os
import chromadb
from langchain_chroma import Chroma
from langchain_core.documents import Document
from src.ollama_utils import get_ollama_embeddings

VECTOR_DB_PATH = "vector_db"

def get_vector_store(persist_directory: str = VECTOR_DB_PATH) -> Chroma:
    embeddings = get_ollama_embeddings()
    return Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
        client_settings=chromadb.Settings(
            anonymized_telemetry=False
        )
    )

def add_documents_to_vector_store(documents: list, persist_directory: str = VECTOR_DB_PATH) -> None:
    vector_store = get_vector_store(persist_directory)
    vector_store.add_documents(documents)
    vector_store.persist()

def get_retriever(k: int = 3, persist_directory: str = VECTOR_DB_PATH):
    vector_store = get_vector_store(persist_directory)
    return vector_store.as_retriever(search_kwargs={"k": k})

def query_vector_store(query: str, k: int = 3, persist_directory: str = VECTOR_DB_PATH) -> list:
    retriever = get_retriever(k, persist_directory)
    results = retriever.get_relevant_documents(query)
    return results

def get_vector_store_stats(persist_directory: str = VECTOR_DB_PATH) -> dict:
    try:
        vector_store = get_vector_store(persist_directory)
        count = vector_store._collection.count()
        return {"document_count": count}
    except Exception as e:
        return {"error": str(e), "document_count": 0}

def clear_vector_store(persist_directory: str = VECTOR_DB_PATH) -> None:
    vector_store = get_vector_store(persist_directory)
    vector_store.delete_collection()

if __name__ == "__main__":
    sample_docs = [
        Document(
            page_content="Natural language processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence.",
            metadata={"source": "test.txt", "chunk_index": 0}
        ),
        Document(
            page_content="Machine learning is a subset of artificial intelligence that provides systems the ability to automatically learn and improve from experience.",
            metadata={"source": "test.txt", "chunk_index": 1}
        )
    ]
    add_documents_to_vector_store(sample_docs)
    results = query_vector_store("What is NLP?", k=2)
    print(f"Query results:")
    for i, doc in enumerate(results):
        print(f"{i+1}. {doc.page_content}")
