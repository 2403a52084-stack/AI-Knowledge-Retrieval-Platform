from src.analytics.analytics_store import (
    save_query_analytics,
    get_all_analytics,
    get_query_count,
    get_analytics_summary
)


save_query_analytics(
    query="What is cloud computing?",
    query_type="factual",
    routing="retrieval_and_answer",
    status="success",
    confidence="High",
    confidence_score=0.72,
    clarification_required=False,
    response_time_ms=150.5,
    domain="Technology",
    retrieved_sources=[
        {
            "source": "cloud_computing.txt",
            "chunk_id": "chunk_1",
            "relevance_score": 0.72
        }
    ]
)


print("\n--- ANALYTICS RECORDS ---")
records = get_all_analytics()

for record in records:
    print(record)


print("\n--- QUERY COUNT ---")
print(get_query_count())


print("\n--- ANALYTICS SUMMARY ---")
print(get_analytics_summary())