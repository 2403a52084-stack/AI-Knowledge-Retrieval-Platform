class QueryUnderstandingAgent:
    """
    Understands and analyzes the user's query.
    """

    def process(self, query):

        query = query.strip()

        if not query:
            return {
                "query": "",
                "intent": "empty",
                "needs_clarification": True
            }

        words = query.split()

        if len(words) <= 2:
            intent = "short_query"
            needs_clarification = True

        elif "?" in query:
            intent = "question"
            needs_clarification = False

        else:
            intent = "general_query"
            needs_clarification = False

        return {
            "query": query,
            "intent": intent,
            "needs_clarification": needs_clarification
        }