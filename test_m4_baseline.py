import time

from src.agents.orchestrator import Orchestrator


# ============================================================
# M4.3 BASELINE EVALUATION
# ============================================================

tests = [
    {
        "domain": "education",
        "query": "What is the minimum attendance percentage required?"
    },
    {
        "domain": "technology",
        "query": "What is cloud computing?"
    },
    {
        "domain": "finance",
        "query": "What is a savings account?"
    },
    {
        "domain": "finance",
        "query": "What is the difference between a savings account and a fixed deposit?"
    }
]


results = []

print("=" * 70)
print("M4.3 BASELINE EVALUATION")
print("=" * 70)


for i, test in enumerate(tests, start=1):

    orchestrator = Orchestrator()

    query = test["query"]
    expected_domain = test["domain"]

    start = time.perf_counter()

    result = orchestrator.process_query(
        query
    )

    elapsed_ms = (
        time.perf_counter() - start
    ) * 1000

    retrieval = result.get(
        "retrieval",
        {}
    )

    retrieved_results = retrieval.get(
        "results",
        []
    )

    top_domain = "Unknown"
    top_score = None

    if retrieved_results:

        first = retrieved_results[0]

        metadata = first.get(
            "metadata",
            {}
        )

        top_domain = str(
            metadata.get(
                "domain",
                "Unknown"
            )
        ).lower()

        top_score = first.get(
            "relevance_score"
        )

    correct = (
        top_domain == expected_domain
    )

    results.append({
        "query": query,
        "expected_domain": expected_domain,
        "top_domain": top_domain,
        "top_score": top_score,
        "response_time_ms": elapsed_ms,
        "correct": correct
    })

    print("\nTEST", i)
    print("Query:", query)
    print("Expected Domain:", expected_domain)
    print("Retrieved Domain:", top_domain)
    print("Top Relevance Score:", top_score)
    print(
        "Response Time:",
        round(elapsed_ms, 2),
        "ms"
    )
    print(
        "Result:",
        "PASS" if correct else "FAIL"
    )


# ============================================================
# CALCULATE BASELINE METRICS
# ============================================================

total = len(results)

correct_count = sum(
    1
    for r in results
    if r["correct"]
)

accuracy = (
    correct_count / total
) * 100


avg_response_time = (
    sum(
        r["response_time_ms"]
        for r in results
    )
    / total
)


scores = [
    r["top_score"]
    for r in results
    if r["top_score"] is not None
]

avg_relevance = (
    sum(scores) / len(scores)
    if scores
    else 0
)


# ============================================================
# FINAL BASELINE
# ============================================================

print("\n" + "=" * 70)
print("BASELINE METRICS")
print("=" * 70)

print(
    "Domain Retrieval Accuracy:",
    round(accuracy, 2),
    "%"
)

print(
    "Average Top-1 Relevance:",
    round(avg_relevance, 4)
)

print(
    "Average Response Time:",
    round(avg_response_time, 2),
    "ms"
)

print("=" * 70)