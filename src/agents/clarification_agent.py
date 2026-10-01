class ClarificationAgent:

    def __init__(self):
        pass

    def analyze_query(self, query):

        query = str(query).strip()

        if not query:
            return {
                "needs_clarification": True,
                "reason": "empty_query",
                "original_query": query,
                "follow_up_question": "What would you like to know?"
            }

        text = query.lower()
        words = query.split()

        # Incomplete or very short query
        if len(words) <= 2:
            return {
                "needs_clarification": True,
                "reason": "incomplete_query",
                "original_query": query,
                "follow_up_question": (
                    f"Could you specify what you would like to know about '{query}'?"
                )
            }

        # Missing context
        context_terms = [
            "what about it",
            "tell me more",
            "explain more",
            "what about this",
            "how about this",
            "what does this mean",
            "explain this"
        ]

        if any(term in text for term in context_terms):
            return {
                "needs_clarification": True,
                "reason": "missing_context",
                "original_query": query,
                "follow_up_question": (
                    "Could you specify which topic or concept you are referring to?"
                )
            }

        # Context-dependent expressions
        if (
            text.startswith("how does it")
            or text.startswith("why does it")
            or text.startswith("what is it")
            or text.startswith("where is it")
        ):
            return {
                "needs_clarification": True,
                "reason": "missing_context",
                "original_query": query,
                "follow_up_question": (
                    "Could you specify the topic or concept you are referring to?"
                )
            }

        # Multi-part query
        multi_part_markers = [
            " and ",
            " also ",
            " as well as ",
            " along with ",
            " plus "
        ]

        marker_count = sum(
            1 for marker in multi_part_markers if marker in text
        )

        multiple_questions = query.count("?") > 1

        if marker_count >= 2 or multiple_questions:
            return {
                "needs_clarification": True,
                "reason": "multi_part_query",
                "original_query": query,
                "follow_up_question": (
                    "Your question contains multiple requirements. "
                    "Would you like me to address all of them together?"
                )
            }

        # Unclear references
        unclear_terms = [
            "thing",
            "stuff",
            "something",
            "it",
            "this",
            "that",
            "they",
            "them"
        ]

        if len(words) <= 5 and any(
            term in text.split()
            for term in unclear_terms
        ):
            return {
                "needs_clarification": True,
                "reason": "unclear_reference",
                "original_query": query,
                "follow_up_question": (
                    "Could you provide more details about the topic you are referring to?"
                )
            }

        # Clear query
        return {
            "needs_clarification": False,
            "reason": "clear_query",
            "original_query": query,
            "follow_up_question": None
        }

    def generate_clarification(self, query):

        result = self.analyze_query(query)

        return result.get(
            "follow_up_question"
        )

    def refine_query(
        self,
        original_query,
        clarification_response
    ):

        original_query = str(
            original_query
        ).strip()

        clarification_response = str(
            clarification_response
        ).strip()

        if not original_query:
            return clarification_response

        if not clarification_response:
            return original_query

        return (
            f"{original_query}. "
            f"Additional clarification: "
            f"{clarification_response}"
        )

    def process(self, query):

        return self.analyze_query(query)
