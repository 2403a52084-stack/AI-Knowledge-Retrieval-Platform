import sys
import os

# Add src to Python path
SRC_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "src"
)

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


from agents.query_understanding_agent import QueryUnderstandingAgent
from agents.retrieval_agent import RetrievalAgent
from agents.response_generation_agent import ResponseGenerationAgent
from agents.clarification_agent import ClarificationAgent
from agents.memory_agent import ConversationMemoryAgent


# ============================================================
# INITIALIZE AGENTS
# ============================================================

query_agent = QueryUnderstandingAgent()
retrieval_agent = RetrievalAgent()
response_agent = ResponseGenerationAgent()
clarification_agent = ClarificationAgent()
memory_agent = ConversationMemoryAgent()


# ============================================================
# PROCESS QUERY
# ============================================================

def process_query(query):

    print("\n" + "=" * 60)
    print("MULTI-AGENT QUERY RESOLUTION")
    print("=" * 60)

    print("\n[1] Query Understanding Agent")

    query_info = query_agent.process(query)

    print("Intent:", query_info["intent"])


    # --------------------------------------------------------
    # Clarification
    # --------------------------------------------------------

    if query_info["needs_clarification"]:

        print("\n[2] Clarification Agent")

        question = clarification_agent.generate_question(
            query
        )

        print("Clarification:", question)

        return


    # --------------------------------------------------------
    # Retrieval
    # --------------------------------------------------------

    print("\n[2] Retrieval Agent")

    results = retrieval_agent.retrieve(
        query_info["query"],
        top_k=3
    )

    print(
        "Retrieved results:",
        len(results)
    )


    # --------------------------------------------------------
    # Response generation
    # --------------------------------------------------------

    print("\n[3] Response Generation Agent")

    answer = response_agent.generate(
        query_info["query"],
        results
    )

    print("\nAnswer:")
    print(answer)


    # --------------------------------------------------------
    # Memory
    # --------------------------------------------------------

    memory_agent.add_interaction(
        query_info["query"],
        answer
    )

    print("\n[4] Conversation Memory Agent")

    print(
        "Conversation items stored:",
        len(memory_agent.get_history())
    )


# ============================================================
# MAIN PROGRAM
# ============================================================

print("=" * 60)
print("AI KNOWLEDGE RETRIEVAL PLATFORM")
print("Multi-Agent Command Line Application")
print("=" * 60)

while True:

    query = input(
        "\nEnter your question "
        "(type 'exit' to quit): "
    )

    if query.lower() == "exit":
        print("\nExiting application.")
        break

    process_query(query)