import chromadb

from embeddings import generate_embeddings, load_embedding_model


DB_PATH = "chroma_db"
COLLECTION_NAME = "knowledge_base"


# Load embedding model
model = load_embedding_model()


# Connect to ChromaDB
client = chromadb.PersistentClient(
    path=DB_PATH
)


def search(query, top_k=3):

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    # Generate embedding for the question
    query_embedding = generate_embeddings(
        model,
        [query]
    )

    # Search ChromaDB
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    formatted_results = []

    for index, document in enumerate(documents):

        metadata = metadatas[index] if index < len(metadatas) else {}
        distance = distances[index] if index < len(distances) else None

        formatted_results.append({
            "text": document,
            "metadata": metadata,
            "distance": distance
        })

    return formatted_results


if __name__ == "__main__":

    print("=" * 60)
    print("RAG RETRIEVAL TEST")
    print("=" * 60)

    query = input("\nEnter your question: ")

    results = search(
        query,
        top_k=3
    )

    print("\n" + "=" * 60)
    print("RETRIEVED RESULTS")
    print("=" * 60)

    for index, result in enumerate(results):

        metadata = result["metadata"]

        print(f"\n--- RESULT {index + 1} ---")

        print(
            "Source:",
            metadata.get("source", "Unknown")
        )

        print(
            "Chunk Index:",
            metadata.get("chunk_index", "N/A")
        )

        if result["distance"] is not None:

            print(
                f"Distance: {result['distance']:.4f}"
            )

        print("\nText:")
        print(result["text"])