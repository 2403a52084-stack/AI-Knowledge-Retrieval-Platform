from pathlib import Path

from document_loader import load_document
from text_cleaner import clean_text
from chunking import split_text
from embeddings import load_embedding_model, generate_embeddings
from vector_store import create_vector_store, add_documents


DATA_FOLDER = "data"


def ingest_knowledge_base():

    print("=" * 60)
    print("STARTING KNOWLEDGE BASE INGESTION")
    print("=" * 60)

    # Load embedding model
    model = load_embedding_model()

    # Create ChromaDB collection
    collection = create_vector_store()

    all_chunks = []
    all_metadatas = []
    all_ids = []

    # Find supported files
    supported_extensions = {
        ".pdf",
        ".docx",
        ".txt",
        ".csv"
    }

    files = []

    for file_path in Path(DATA_FOLDER).rglob("*"):

        if file_path.suffix.lower() in supported_extensions:
            files.append(file_path)

    print(f"\nFound {len(files)} documents.")

    # Process every document
    for file_path in files:

        print("\n" + "-" * 60)
        print(f"Processing: {file_path}")

        try:

            # 1. Load document
            text = load_document(file_path)

            # 2. Clean text
            cleaned_text = clean_text(text)

            # 3. Split into chunks
            chunks = split_text(cleaned_text)

            print(f"Created {len(chunks)} chunks.")

            # 4. Store chunks and metadata
            for index, chunk in enumerate(chunks):

                all_chunks.append(chunk)

                all_metadatas.append({
                    "source": str(file_path),
                    "filename": file_path.name,
                    "domain": file_path.parent.name,
                    "chunk_index": index
                })

                all_ids.append(
                    f"{file_path.stem}_{index}"
                )

        except Exception as error:

            print(f"ERROR: {error}")

    # Generate embeddings for all chunks
    print("\n" + "=" * 60)
    print("GENERATING EMBEDDINGS")
    print("=" * 60)

    embeddings = generate_embeddings(
        model,
        all_chunks
    )

    print(
        f"Generated embeddings for {len(all_chunks)} chunks."
    )

    # Store everything in ChromaDB
    print("\n" + "=" * 60)
    print("STORING DATA IN CHROMADB")
    print("=" * 60)

    add_documents(
        collection,
        all_chunks,
        embeddings,
        all_metadatas,
        all_ids
    )

    print("\n" + "=" * 60)
    print("INGESTION COMPLETED")
    print("=" * 60)

    print(
        "Total chunks in database:",
        collection.count()
    )


if __name__ == "__main__":
    ingest_knowledge_base()