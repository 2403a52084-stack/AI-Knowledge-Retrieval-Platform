class ClarificationAgent:
    """
    Handles unclear or incomplete user queries.
    """

    def generate_question(self, query):
        return (
            "Could you please provide more details "
            "about your question?"
        )