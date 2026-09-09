class ConversationMemoryAgent:
    """
    Stores previous questions and answers
    during the current session.
    """

    def __init__(self):
        self.history = []

    def add_interaction(self, query, answer):
        self.history.append({
            "query": query,
            "answer": answer
        })

    def get_history(self):
        return self.history

    def clear(self):
        self.history = []