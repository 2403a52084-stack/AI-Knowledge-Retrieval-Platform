import os

import chromadb
from sentence_transformers import SentenceTransformer


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")

MODEL_NAME = "all-MiniLM-L6-v2"


embedding_model = SentenceTransformer(MODEL_NAME)

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_collection(
    name="knowledge_base"
)


def retrieve(query, top_k=3):
    """
    Retrieve the most relevant chunks from the knowledge base.
    """

    query = str(query).strip()

    if not query:
        return []

    query_embedding = embedding_model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results.get("documents", [[]])
    metadatas = results.get("metadatas", [[]])
    distances = results.get("distances", [[]])

    documents = documents[0] if documents else []
    metadatas = metadatas[0] if metadatas else []
    distances = distances[0] if distances else []

    retrieved = []

    for i, document in enumerate(documents):

        metadata = (
            metadatas[i]
            if i < len(metadatas)
            else {}
        )

        distance = (
            distances[i]
            if i < len(distances)
            else None
        )

        retrieved.append({
            "text": document,
            "metadata": metadata,
            "distance": distance
        })

    return retrieved