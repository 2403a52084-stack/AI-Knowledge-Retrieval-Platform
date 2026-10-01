from .clarification_agent import ClarificationAgent
from .memory_agent import ConversationMemoryAgent
from .query_understanding_agent import QueryUnderstandingAgent
from .retrieval_agent import RetrievalAgent
from .response_generation_agent import ResponseGenerationAgent


class Orchestrator:

    def __init__(self):

        self.clarification_agent = ClarificationAgent()

        self.memory_agent = ConversationMemoryAgent(
            max_history=10
        )

        self.query_agent = QueryUnderstandingAgent()

        self.retrieval_agent = RetrievalAgent(
            top_k=3,
            confidence_threshold=0.40
        )

        self.response_agent = ResponseGenerationAgent()


    def process_query(
        self,
        query,
        clarification_response=None
    ):

        query = str(query).strip()

        if not query:
            return {
                "query": query,
                "status": "error",
                "message": "No query was provided."
            }


        # ======================================================
        # M3.2 CONVERSATION MEMORY
        # ======================================================

        memory_context = (
            self.memory_agent.build_context(
                query
            )
        )


        # ======================================================
        # M3.1 CLARIFICATION
        # ======================================================

        clarification = (
            self.clarification_agent.process(
                query
            )
        )


        # ======================================================
        # CLARIFICATION REQUIRED
        # ======================================================

        if (
            clarification.get(
                "needs_clarification",
                False
            )
            and not memory_context
            and not clarification_response
        ):

            return {
                "query": query,
                "status": "clarification_required",
                "clarification": clarification,
                "message": clarification.get(
                    "follow_up_question",
                    "Please provide more details."
                )
            }


        # ======================================================
        # REFINE USING CLARIFICATION
        # ======================================================

        if clarification_response:

            refined_query = (
                self.clarification_agent.refine_query(
                    query,
                    clarification_response
                )
            )

        else:

            refined_query = query


        # ======================================================
        # ADD MEMORY CONTEXT FOR FOLLOW-UP QUESTIONS
        # ======================================================

        resolution_query = refined_query


        if memory_context:

            resolution_query = (
                f"{refined_query}\n\n"
                f"Conversation Context:\n"
                f"{memory_context}"
            )


        # ======================================================
        # M2.1 QUERY UNDERSTANDING
        # ======================================================

        try:

            classification = (
                self.query_agent.process_query(
                    resolution_query
                )
            )

        except Exception as error:

            return {
                "query": query,
                "refined_query": refined_query,
                "status": "classification_error",
                "message": (
                    f"Query classification failed: {error}"
                )
            }


        query_type = classification.get(
            "query_type",
            "ambiguous"
        )


        # ======================================================
        # M2.2 RETRIEVAL
        # ======================================================

        try:

            retrieval_result = (
                self.retrieval_agent.process_query(
                    resolution_query,
                    query_type=query_type
                )
            )

        except Exception as error:

            return {
                "query": query,
                "refined_query": refined_query,
                "query_type": query_type,
                "classification": classification,
                "status": "retrieval_error",
                "message": (
                    f"Retrieval failed: {error}"
                )
            }


        # ======================================================
        # M2.3 RESPONSE GENERATION
        # ======================================================

        try:

            response_result = (
                self.response_agent.process_query(
                    resolution_query,
                    retrieval_result
                )
            )

        except Exception as error:

            return {
                "query": query,
                "refined_query": refined_query,
                "query_type": query_type,
                "classification": classification,
                "retrieval": retrieval_result,
                "status": "response_error",
                "message": (
                    f"Response generation failed: {error}"
                )
            }


        # ======================================================
        # STORE CONVERSATION MEMORY
        # ======================================================

        self.memory_agent.add_turn(
            query=query,
            response=response_result.get(
                "answer"
            ),
            clarification=clarification_response,
            sources=response_result.get(
                "sources",
                []
            ),
            topic=query_type
        )


        # ======================================================
        # FINAL RESPONSE
        # ======================================================

        return {
            "query": query,

            "refined_query": refined_query,

            "resolution_query": resolution_query,

            "memory_context": memory_context,

            "query_type": query_type,

            "classification": classification,

            "clarification": clarification,

            "retrieval": retrieval_result,

            "response": response_result,

            "answer": response_result.get(
                "answer"
            ),

            "confidence": response_result.get(
                "confidence"
            ),

            "confidence_score": response_result.get(
                "confidence_score"
            ),

            "sources": response_result.get(
                "sources",
                []
            ),

            "status": response_result.get(
                "status",
                "success"
            )
        }
