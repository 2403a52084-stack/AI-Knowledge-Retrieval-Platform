import time

from src.agents.retrieval_agent import RetrievalAgent


# ============================================================
# M4.3 OPTIMIZED RETRIEVAL EVALUATION
# ============================================================

tests = [
    {
        "domain": "education",
        "query": "What is the minimum attendance percentage required?",
        "query_type": "factual"
    },
    {
        "domain": "technology",
        "query": "What is cloud computing?",
        "query_type": "factual"
    },
    {
        "domain": "finance",
        "query": "What is a savings account?",
        "query_type": "factual"
    },
    {
        "domain": "finance",
        "query": "What is the difference between a savings account and a fixed deposit?",
        "query_type": "comparative"
    }
]


# Optimized configuration
agent = RetrievalAgent(
    top_k=2,
    confidence_threshold=0.55
)


results = []

print("=" * 70)
print("M4.3 OPTIMIZED RETRIEVAL EVALUATION")
print("=" * 70)

print("Configuration:")
print("Top-K:", agent.top_k)
print("Confidence Threshold:", agent.confidence_threshold)


for i, test in enumerate(tests, start=1):

    query = test["query"]
    expected_domain = test["domain"]

    start = time.perf_counter()

    result = agent.process_query(
        query,
        query_type=test["query_type"]
    )

    elapsed_ms = (
        time.perf_counter() - start
    ) * 1000

    retrieved_results = result.get(
        "results",
        []
    )

    correct_domain = False

    relevance_scores = []

    for item in retrieved_results:

        metadata = item.get(
            "metadata",
            {}
        )

        domain = str(
            metadata.get(
                "domain",
                "Unknown"
            )
        ).lower()

        score = item.get(
            "relevance_score"
        )

        if score is not None:
            relevance_scores.append(
                float(score)
            )

        if domain == expected_domain:
            correct_domain = True

    average_relevance = (
        sum(relevance_scores)
        / len(relevance_scores)
        if relevance_scores
        else 0
    )

    passed = (
        result.get("status") == "success"
        and correct_domain
    )

    results.append({
        "query": query,
        "expected_domain": expected_domain,
        "retrieved_count": len(
            retrieved_results
        ),
        "average_relevance":
            average_relevance,
        "response_time_ms":
            elapsed_ms,
        "passed":
            passed
    })


    print("\n" + "-" * 70)
    print("TEST", i)
    print("-" * 70)

    print(
        "Query:",
        query
    )

    print(
        "Expected Domain:",
        expected_domain
    )

    print(
        "Retrieved Chunks:",
        len(retrieved_results)
    )

    for item in retrieved_results:

        metadata = item.get(
            "metadata",
            {}
        )

        print(
            "Source:",
            metadata.get(
                "source",
                metadata.get(
                    "filename",
                    "Unknown"
                )
            )
        )

        print(
            "Domain:",
            metadata.get(
                "domain",
                "Unknown"
            )
        )

        print(
            "Relevance:",
            item.get(
                "relevance_score"
            )
        )

    print(
        "Average Retrieved Relevance:",
        round(
            average_relevance,
            4
        )
    )

    print(
        "Response Time:",
        round(
            elapsed_ms,
            2
        ),
        "ms"
    )

    print(
        "Result:",
        "PASS" if passed else "FAIL"
    )


# ============================================================
# OPTIMIZED METRICS
# ============================================================

total = len(results)

passed_count = sum(
    1
    for r in results
    if r["passed"]
)

accuracy = (
    passed_count / total
) * 100

average_relevance = (
    sum(
        r["average_relevance"]
        for r in results
    )
    / total
)

average_response_time = (
    sum(
        r["response_time_ms"]
        for r in results
    )
    / total
)

average_chunks = (
    sum(
        r["retrieved_count"]
        for r in results
    )
    / total
)


# ============================================================
# FINAL RESULTS
# ============================================================

print("\n" + "=" * 70)
print("M4.3 OPTIMIZED METRICS")
print("=" * 70)

print(
    "Domain Retrieval Accuracy:",
    round(
        accuracy,
        2
    ),
    "%"
)

print(
    "Average Retrieved Relevance:",
    round(
        average_relevance,
        4
    )
)

print(
    "Average Retrieved Chunks:",
    round(
        average_chunks,
        2
    )
)

print(
    "Average Response Time:",
    round(
        average_response_time,
        2
    ),
    "ms"
)

print("=" * 70)