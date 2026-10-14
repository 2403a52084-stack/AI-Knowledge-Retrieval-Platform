import chromadb


DB_PATH = "chroma_db"
COLLECTION_NAME = "knowledge_base"


client = chromadb.PersistentClient(
    path=DB_PATH
)

collection = client.get_collection(
    name=COLLECTION_NAME
)


print("=" * 60)
print("BEFORE CLEANUP")
print("=" * 60)

total_before = collection.count()

print(
    "Total chunks:",
    total_before
)


# Get all metadata and IDs
data = collection.get(
    include=["metadatas"]
)

ids_to_delete = []


for i, metadata in enumerate(
    data["metadatas"]
):

    domain = str(
        metadata.get("domain", "")
    ).strip().lower()


    # Delete records where the domain field
    # is missing or explicitly marked unknown.
    if not domain or domain == "unknown":

        ids_to_delete.append(
            data["ids"][i]
        )


print(
    "Unknown/missing-domain chunks found:",
    len(ids_to_delete)
)


# Delete unwanted records
if ids_to_delete:

    collection.delete(
        ids=ids_to_delete
    )

    print(
        "Deleted:",
        len(ids_to_delete),
        "old chunks."
    )

else:

    print(
        "No unknown/missing-domain chunks found."
    )


print("\n" + "=" * 60)
print("AFTER CLEANUP")
print("=" * 60)

print(
    "Total chunks:",
    collection.count()
)