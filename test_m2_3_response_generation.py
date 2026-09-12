from src.agents.response_generation_agent import ResponseGenerationAgent


agent = ResponseGenerationAgent()


retrieval_result = {
    "status": "success",
    "results": [
        {
            "text": (
                "Students are required to maintain a minimum "
                "attendance percentage of 75 percent."
            ),
            "source": "data\\education\\attendance_policy.pdf",
            "chunk_id": 0,
            "page": "Unknown",
            "relevance_score": 0.5819,
            "metadata": {
                "source": "data\\education\\attendance_policy.pdf",
                "chunk_index": 0
            }
        }
    ]
}


result = agent.process_query(
    "What is the minimum attendance requirement?",
    retrieval_result
)


print("=" * 60)
print("M2.3 RESPONSE GENERATION TEST")
print("=" * 60)

print("Question:", result["query"])
print("Answer:", result["answer"])
print("Confidence:", result["confidence"])
print("Confidence Score:", result["confidence_score"])
print("Status:", result["status"])

print("\nSources:")

for source in result["sources"]:
    print("Source:", source["source"])
    print("Chunk:", source["chunk_id"])
    print("Page:", source["page"])
    print("Relevance:", source["relevance_score"])