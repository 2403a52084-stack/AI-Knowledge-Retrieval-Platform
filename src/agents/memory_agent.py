class ConversationMemoryAgent:

    def __init__(self, max_history=10):
        self.max_history = max_history
        self.history = []

    # ==========================================================
    # ADD CONVERSATION
    # ==========================================================

    def add_turn(
        self,
        query,
        response=None,
        clarification=None,
        sources=None,
        topic=None
    ):

        turn = {
            "query": str(query).strip(),
            "response": response,
            "clarification": clarification,
            "sources": sources or [],
            "topic": topic
        }

        self.history.append(turn)

        # Keep only recent conversations
        if len(self.history) > self.max_history:
            self.history = self.history[
                -self.max_history:
            ]

    # ==========================================================
    # GET HISTORY
    # ==========================================================

    def get_history(self):

        return list(self.history)

    # ==========================================================
    # FIND RELEVANT CONTEXT
    # ==========================================================

    def get_relevant_context(self, query):

        query = str(query).lower().strip()

        if not query:
            return []

        relevant = []

        query_words = set(
            word.strip(".,?!")
            for word in query.split()
            if len(word) > 2
        )

        for turn in reversed(self.history):

            previous_query = str(
                turn.get("query", "")
            ).lower()

            previous_topic = str(
                turn.get("topic", "")
            ).lower()

            previous_words = set(
                word.strip(".,?!")
                for word in (
                    previous_query + " " + previous_topic
                ).split()
                if len(word) > 2
            )

            # Word overlap
            overlap = query_words.intersection(
                previous_words
            )

            # Follow-up/context words
            follow_up_words = [
                "it",
                "this",
                "that",
                "they",
                "them",
                "its",
                "these",
                "those",
                "more"
            ]

            is_follow_up = any(
                word in query_words
                for word in follow_up_words
            )

            if overlap or is_follow_up:

                relevant.append(turn)

        return relevant[:3]

    # ==========================================================
    # CONTEXT SUMMARY
    # ==========================================================

    def build_context(self, query):

        relevant_turns = self.get_relevant_context(
            query
        )

        if not relevant_turns:
            return ""

        context_parts = []

        for turn in relevant_turns:

            context_parts.append(
                "Previous Query: "
                + str(turn.get("query", ""))
            )

            if turn.get("response"):

                context_parts.append(
                    "Previous Response: "
                    + str(turn.get("response", ""))
                )

            if turn.get("topic"):

                context_parts.append(
                    "Topic: "
                    + str(turn.get("topic", ""))
                )

        return "\n".join(
            context_parts
        )

    # ==========================================================
    # CLEAR MEMORY
    # ==========================================================

    def clear_memory(self):

        self.history.clear()

    # ==========================================================
    # MEMORY STATUS
    # ==========================================================

    def memory_size(self):

        return len(self.history)