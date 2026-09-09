from retriever import search


class RetrievalAgent:
    """
    Retrieves relevant information from the knowledge base.
    """

    def retrieve(self, query, top_k=3):
        return search(
            query,
            top_k=top_k
        )