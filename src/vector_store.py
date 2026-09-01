import chromadb

DB_PATH = "chroma_db"
COLLECTION_NAME = "knowledge_base"


def create_vector_store():
    """Create or open the ChromaDB collection."""

    client = chromadb.PersistentClient(
        path=DB_PATH
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    print("ChromaDB collection:", COLLECTION_NAME)
    print("Current chunks:", collection.count())

    return collection


def add_documents(
    collection,
    chunks,
    embeddings,
    metadatas,
    ids
):
    """Add document chunks and embeddings to ChromaDB."""

    if not chunks:
        print("ERROR: No chunks to add.")
        return

    # Correct check for NumPy embeddings
    if embeddings is None or len(embeddings) == 0:
        print("ERROR: No embeddings to add.")
        return

    # Convert NumPy array to Python list
    if hasattr(embeddings, "tolist"):
        embeddings = embeddings.tolist()

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"Added {len(chunks)} chunks to ChromaDB.")
    print(
        "Total chunks in collection:",
        collection.count()
    )