from src.agents.orchestrator import Orchestrator


orchestrator = Orchestrator()


queries = [
    "What is the minimum attendance requirement?",
    "What is cloud computing?",
    "What is the difference between AI and machine learning?",
    "What is the hostel fee?"
]


for query in queries:

    print("\n" + "=" * 70)
    print("QUESTION:", query)

    result = orchestrator.process_query(query)

    print("Query Type:", result.get("query_type"))
    print("Status:", result.get("status"))
    print("Answer:", result.get("answer"))
    print("Confidence:", result.get("confidence"))
    print("Confidence Score:", result.get("confidence_score"))

    print("\nSources:")

    for source in result.get("sources", []):
        print(
            source.get("source"),
            "| Chunk:",
            source.get("chunk_id"),
            "| Relevance:",
            source.get("relevance_score")
        )