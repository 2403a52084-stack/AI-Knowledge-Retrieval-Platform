from src.agents.retrieval_agent import RetrievalAgent


agent = RetrievalAgent(
    top_k=3,
    confidence_threshold=0.60
)


test_queries = [
    ("What is the minimum attendance requirement?", "factual"),
    ("What is cloud computing?", "factual"),
    ("How is attendance calculated?", "procedural"),
    ("What is the difference between AI and machine learning?", "comparative"),
    ("What is the hostel fee?", "factual")
]


for query, query_type in test_queries:

    print("\n" + "=" * 60)
    print("Question:", query)
    print("Query Type:", query_type)

    result = agent.process_query(
        query,
        query_type=query_type
    )

    print("Status:", result.get("status"))
    print("Message:", result.get("message"))

    for item in result.get("results", []):

        print("\nRank:", item.get("rank"))
        print("Relevance Score:", item.get("relevance_score"))
        print("Source:", item.get("source"))
        print("Chunk:", item.get("chunk_id"))
        print("Page:", item.get("page"))

        text = item.get("text", "")
        print("Text:", text[:200])