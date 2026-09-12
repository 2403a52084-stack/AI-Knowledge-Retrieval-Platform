from src.query_understanding_agent import QueryUnderstandingAgent


agent = QueryUnderstandingAgent()

test_queries = [
    "What is cloud computing?",
    "How is attendance calculated?",
    "What is the difference between AI and machine learning?",
    "Tell me about attendance.",
    "What is the minimum attendance requirement?"
]

for query in test_queries:
    result = agent.process_query(query)

    print("\nQuestion:", query)
    print("Type:", result["query_type"])
    print("Confidence:", result["classification_confidence"])
    print("Routing:", result["routing"])