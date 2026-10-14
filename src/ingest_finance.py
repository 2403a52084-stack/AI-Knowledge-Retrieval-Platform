from pathlib import Path

from document_loader import load_document
from text_cleaner import clean_text
from chunking import split_text
from embeddings import load_embedding_model, generate_embeddings
from vector_store import create_vector_store, add_documents


# ============================================================
# FINANCE DATA FOLDER
# ============================================================

FINANCE_FOLDER = Path("data/finance")


# ============================================================
# INGEST FINANCE DOCUMENTS
# ============================================================

def ingest_finance():

    print("=" * 60)
    print("INGESTING FINANCE DOMAIN")
    print("=" * 60)

    # Load embedding model
    model = load_embedding_model()

    # Open ChromaDB collection
    collection = create_vector_store()

    # Supported files
    supported_extensions = {
        ".txt",
        ".csv"
    }

    # Find Finance files
    files = [
        file_path
        for file_path in FINANCE_FOLDER.rglob("*")
        if file_path.suffix.lower() in supported_extensions
    ]

    print(f"Found {len(files)} Finance files.")

    if not files:
        print("No Finance files found.")
        return

    all_chunks = []
    all_metadatas = []
    all_ids = []

    # ========================================================
    # PROCESS FILES
    # ========================================================

    for file_path in files:

        print("\nProcessing:", file_path)

        try:

            # Load document
            text = load_document(
                file_path
            )

            # Clean text
            cleaned_text = clean_text(
                text
            )

            # Split into chunks
            chunks = split_text(
                cleaned_text
            )

            print(
                "Created",
                len(chunks),
                "chunks."
            )

            # Store chunks and metadata
            for index, chunk in enumerate(chunks):

                all_chunks.append(
                    chunk
                )

                all_metadatas.append({
                    "source": str(file_path),
                    "filename": file_path.name,
                    "domain": "finance",
                    "chunk_index": index
                })

                all_ids.append(
                    f"finance_{file_path.stem}_{index}"
                )

        except Exception as error:

            print(
                "ERROR:",
                error
            )


    # ========================================================
    # CHECK CHUNKS
    # ========================================================

    if not all_chunks:

        print(
            "No Finance chunks were created."
        )

        return


    # ========================================================
    # GENERATE EMBEDDINGS
    # ========================================================

    print(
        "\nGenerating embeddings..."
    )

    embeddings = generate_embeddings(
        model,
        all_chunks
    )

    print(
        f"Generated embeddings for "
        f"{len(all_chunks)} chunks."
    )


    # ========================================================
    # ADD TO CHROMADB
    # ========================================================

    print(
        "\nAdding Finance data to ChromaDB..."
    )

    add_documents(
        collection,
        all_chunks,
        embeddings,
        all_metadatas,
        all_ids
    )


    # ========================================================
    # COMPLETION
    # ========================================================

    print("\n" + "=" * 60)
    print("FINANCE INGESTION COMPLETED")
    print("=" * 60)

    print(
        "Total chunks in database:",
        collection.count()
    )


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":

    ingest_finance()