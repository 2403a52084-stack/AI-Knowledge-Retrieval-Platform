from .query_understanding_agent import QueryUnderstandingAgent
from .retrieval_agent import RetrievalAgent
from .response_generation_agent import ResponseGenerationAgent


class Orchestrator:

    def __init__(self):
        self.query_agent = QueryUnderstandingAgent()
        self.retrieval_agent = RetrievalAgent(
            top_k=3,
            confidence_threshold=0.40
        )
        self.response_agent = ResponseGenerationAgent()

    def process_query(self, query):

        query = str(query).strip()

        if not query:
            return {
                "query": query,
                "status": "error",
                "message": "No query was provided."
            }

        # Step 1: Query Understanding
        try:
            classification = self.query_agent.process_query(query)
        except Exception as error:
            return {
                "query": query,
                "status": "classification_error",
                "message": f"Query classification failed: {error}"
            }

        query_type = classification.get(
            "query_type",
            "ambiguous"
        )

        # Step 2: Retrieval
        try:
            retrieval_result = self.retrieval_agent.process_query(
                query,
                query_type=query_type
            )
        except Exception as error:
            return {
                "query": query,
                "query_type": query_type,
                "classification": classification,
                "status": "retrieval_error",
                "message": f"Retrieval failed: {error}"
            }

        # Step 3: Response Generation
        try:
            response_result = self.response_agent.process_query(
                query,
                retrieval_result
            )
        except Exception as error:
            return {
                "query": query,
                "query_type": query_type,
                "classification": classification,
                "retrieval": retrieval_result,
                "status": "response_error",
                "message": f"Response generation failed: {error}"
            }

        return {
            "query": query,
            "query_type": query_type,
            "classification": classification,
            "retrieval": retrieval_result,
            "response": response_result,
            "answer": response_result.get("answer"),
            "confidence": response_result.get("confidence"),
            "confidence_score": response_result.get(
                "confidence_score"
            ),
            "sources": response_result.get("sources", []),
            "status": response_result.get(
                "status",
                "success"
            )
        }