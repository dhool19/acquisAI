import chromadb
from sentence_transformers import SentenceTransformer

from app.core.config import (
    CHROMA_DB_PATH,
    COLLECTION_NAME,
    EMBEDDING_MODEL_NAME,
)

model = SentenceTransformer(EMBEDDING_MODEL_NAME)

client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)


def retrieve_context(question: str, n_results: int = 5):
    question_embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results,
        include=["documents", "metadatas"]
    )

    chunks = []

    for document, metadata in zip(
        results["documents"][0],
        results["metadatas"][0]
    ):
        chunks.append({
            "text": document,
            "source": metadata.get("source", "unknown"),
            "file_name": metadata.get("file_name", "unknown"),
            "page_number": metadata.get("page_number", "unknown"),
            "chunk_index": metadata.get("chunk_index", "unknown"),
        })

    return chunks