import chromadb
from sentence_transformers import SentenceTransformer


# ------------------------------------------------------------
# CONNECT TO CHROMADB
# ------------------------------------------------------------

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_collection(
    name="knowledge_base"
)


# ------------------------------------------------------------
# LOAD EMBEDDING MODEL
# ------------------------------------------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ------------------------------------------------------------
# TEST FUNCTION
# ------------------------------------------------------------

def test_query(query):

    print("\n" + "=" * 60)
    print("QUERY:", query)
    print("=" * 60)

    embedding = model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=3,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i in range(len(documents)):

        metadata = metadatas[i]

        print("\nResult", i + 1)

        print(
            "Source:",
            metadata.get("source")
        )

        print(
            "Filename:",
            metadata.get("filename")
        )

        print(
            "Domain:",
            metadata.get("domain")
        )

        print(
            "Distance:",
            distances[i]
        )

        print(
            "Text:",
            documents[i][:200].replace(
                "\n",
                " "
            )
        )


# ------------------------------------------------------------
# TEST TECHNOLOGY
# ------------------------------------------------------------

test_query(
    "What is cloud computing?"
)


# ------------------------------------------------------------
# TEST FINANCE
# ------------------------------------------------------------

test_query(
    "What is a savings account?"
)