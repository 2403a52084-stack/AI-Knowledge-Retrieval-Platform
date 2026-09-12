class QueryUnderstandingAgent:

    def process(self, query):
        query = str(query).strip()

        if not query:
            return {
                "query": query,
                "query_type": "ambiguous",
                "classification_confidence": 0.0,
                "routing": "clarification"
            }

        text = query.lower()

        if any(word in text for word in [
            "difference",
            "compare",
            "comparison",
            "versus",
            "vs"
        ]):
            return {
                "query": query,
                "query_type": "comparative",
                "classification_confidence": 0.95,
                "routing": "retrieval_and_comparison"
            }

        if (
            text.startswith("how ")
            or "steps" in text
            or "procedure" in text
            or "process" in text
            or "calculate" in text
            or "method" in text
        ):
            return {
                "query": query,
                "query_type": "procedural",
                "classification_confidence": 0.90,
                "routing": "retrieval_and_procedure"
            }

        if len(query.split()) <= 2:
            return {
                "query": query,
                "query_type": "ambiguous",
                "classification_confidence": 0.60,
                "routing": "clarification"
            }

        return {
            "query": query,
            "query_type": "factual",
            "classification_confidence": 0.85,
            "routing": "retrieval_and_answer"
        }

    def classify_query(self, query):
        return self.process(query)

    def process_query(self, query):
        return self.process(query)
