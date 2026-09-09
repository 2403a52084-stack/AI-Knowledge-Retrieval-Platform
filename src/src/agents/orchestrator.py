from agents.query_understanding_agent import QueryUnderstandingAgent
from agents.retrieval_agent import RetrievalAgent
from agents.response_generation_agent import ResponseGenerationAgent
from agents.clarification_agent import ClarificationAgent
from agents.memory_agent import ConversationMemoryAgent


class MultiAgentOrchestrator:
    """
    Coordinates all agents involved in query resolution.
    """

    def __init__(self):

        self.query_agent = QueryUnderstandingAgent()

        self.retrieval_agent = RetrievalAgent()

        self.response_agent = ResponseGenerationAgent()

        self.clarification_agent = ClarificationAgent()

        self.memory_agent = ConversationMemoryAgent()


    def process_query(self, query):

        # Step 1: Understand the query
        query_info = self.query_agent.process(query)

        # Step 2: Check whether clarification is needed
        if query_info["needs_clarification"]:

            return {
                "answer": self.clarification_agent.generate_question(
                    query
                ),
                "results": [],
                "clarification": True
            }

        # Step 3: Retrieve relevant documents
        results = self.retrieval_agent.retrieve(
            query_info["query"],
            top_k=3
        )

        # Step 4: Generate answer
        answer = self.response_agent.generate(
            query_info["query"],
            results
        )

        # Step 5: Store conversation
        self.memory_agent.add_interaction(
            query_info["query"],
            answer
        )

        return {
            "answer": answer,
            "results": results,
            "clarification": False
        }