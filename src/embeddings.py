from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


def load_embedding_model():
    """
    Load the sentence-transformer embedding model.
    """

    print("Loading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    print("Embedding model loaded successfully.")

    return model


def generate_embeddings(model, texts):
    """
    Generate embeddings for a list of text chunks.
    """

    embeddings = model.encode(
        texts,
        convert_to_numpy=True
    )

    return embeddings


if __name__ == "__main__":

    model = load_embedding_model()

    sample_chunks = [
        "Students must maintain 75 percent attendance.",
        "Artificial intelligence is a field of computer science.",
        "Cloud computing provides computing resources through services."
    ]

    embeddings = generate_embeddings(
        model,
        sample_chunks
    )

    print("\nNumber of chunks:", len(embeddings))

    print("Embedding dimension:", len(embeddings[0]))

    print("\nFirst embedding:")
    print(embeddings[0])