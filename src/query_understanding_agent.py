class QueryUnderstandingAgent:
    """
    Analyzes the user's query and identifies
    basic query characteristics.
    """

    def process(self, query):
        query = query.strip()

        if not query:
            return {
                "query": "",
                "intent": "empty",
                "needs_clarification": True
            }

        if len(query.split()) <= 2:
            intent = "short_query"
        elif "?" in query:
            intent = "question"
        else:
            intent = "general_query"

        return {
            "query": query,
            "intent": intent,
            "needs_clarification": False
        }