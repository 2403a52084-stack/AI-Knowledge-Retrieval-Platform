from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text(text, chunk_size=500, chunk_overlap=50):
    """
    Split cleaned text into overlapping chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = splitter.split_text(text)

    return chunks


if __name__ == "__main__":

    sample_text = """
    Artificial Intelligence is a field of computer science.
    It focuses on creating systems that can perform tasks
    that normally require human intelligence.

    Machine learning is a major part of artificial intelligence.
    Machine learning systems learn patterns from data and use
    those patterns to make predictions or decisions.

    Cloud computing provides computing resources through
    network-accessible services. These resources can include
    servers, storage, databases, and software applications.
    """

    chunks = split_text(sample_text)

    print(f"Total chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks):

        print("\n" + "=" * 50)
        print(f"CHUNK {i + 1}")
        print("=" * 50)
        print(chunk)