import time
from statistics import mean

from src.agents.retrieval_agent import RetrievalAgent


# ---------------------------------------------------------
# TEST QUERIES
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# CONFIGURATIONS
# ---------------------------------------------------------
baseline_agent = RetrievalAgent(
    top_k=3,
    confidence_threshold=0.40
)

optimized_agent = RetrievalAgent(
    top_k=2,
    confidence_threshold=0.55
)


# ---------------------------------------------------------
# WARM-UP
# This prevents first-run model loading from affecting timing.
# ---------------------------------------------------------
print("=" * 75)
print("WARM-UP")
print("=" * 75)

for test in tests:
    baseline_agent.process_query(
        test["query"],
        query_type=test["query_type"]
    )

    optimized_agent.process_query(
        test["query"],
        query_type=test["query_type"]
    )

print("Warm-up completed.\n")


# ---------------------------------------------------------
# BENCHMARK FUNCTION
# ---------------------------------------------------------
def benchmark(agent, config_name, repeats=5):

    print("=" * 75)
    print(config_name)
    print("=" * 75)

    all_results = []

    for i, test in enumerate(tests, start=1):

        times = []
        top1_scores = []
        retrieved_counts = []
        domain_correct_runs = 0

        for _ in range(repeats):

            start = time.perf_counter()

            result = agent.process_query(
                test["query"],
                query_type=test["query_type"]
            )

            elapsed_ms = (time.perf_counter() - start) * 1000
            times.append(elapsed_ms)

            retrieved_results = result.get("results", [])

            retrieved_counts.append(len(retrieved_results))

            # Top-1 relevance
            if retrieved_results:
                top1_score = retrieved_results[0].get(
                    "relevance_score", 0
                )
                top1_scores.append(float(top1_score))

                # Domain check
                top1_metadata = retrieved_results[0].get(
                    "metadata", {}
                )

                top1_domain = str(
                    top1_metadata.get("domain", "Unknown")
                ).lower()

                if top1_domain == test["domain"]:
                    domain_correct_runs += 1

            else:
                top1_scores.append(0)

        avg_time = mean(times)
        avg_top1 = mean(top1_scores)
        avg_chunks = mean(retrieved_counts)

        domain_accuracy = (
            domain_correct_runs / repeats
        ) * 100

        result_data = {
            "query": test["query"],
            "domain_accuracy": domain_accuracy,
            "top1_relevance": avg_top1,
            "avg_chunks": avg_chunks,
            "avg_time": avg_time
        }

        all_results.append(result_data)

        print(f"\nTEST {i}")
        print("-" * 75)
        print("Query:", test["query"])
        print("Expected Domain:", test["domain"])
        print(
            "Domain Accuracy:",
            round(domain_accuracy, 2),
            "%"
        )
        print(
            "Average Top-1 Relevance:",
            round(avg_top1, 4)
        )
        print(
            "Average Retrieved Chunks:",
            round(avg_chunks, 2)
        )
        print(
            "Average Response Time:",
            round(avg_time, 2),
            "ms"
        )

    return all_results


# ---------------------------------------------------------
# RUN BASELINE
# ---------------------------------------------------------
baseline_results = benchmark(
    baseline_agent,
    "BASELINE CONFIGURATION: Top-K=3, Threshold=0.40"
)


# ---------------------------------------------------------
# RUN OPTIMIZED
# ---------------------------------------------------------
optimized_results = benchmark(
    optimized_agent,
    "OPTIMIZED CONFIGURATION: Top-K=2, Threshold=0.55"
)


# ---------------------------------------------------------
# OVERALL METRICS
# ---------------------------------------------------------
baseline_accuracy = mean(
    [r["domain_accuracy"] for r in baseline_results]
)

optimized_accuracy = mean(
    [r["domain_accuracy"] for r in optimized_results]
)

baseline_top1 = mean(
    [r["top1_relevance"] for r in baseline_results]
)

optimized_top1 = mean(
    [r["top1_relevance"] for r in optimized_results]
)

baseline_chunks = mean(
    [r["avg_chunks"] for r in baseline_results]
)

optimized_chunks = mean(
    [r["avg_chunks"] for r in optimized_results]
)

baseline_time = mean(
    [r["avg_time"] for r in baseline_results]
)

optimized_time = mean(
    [r["avg_time"] for r in optimized_results]
)


# ---------------------------------------------------------
# IMPROVEMENT CALCULATIONS
# ---------------------------------------------------------
chunk_reduction = (
    (baseline_chunks - optimized_chunks)
    / baseline_chunks
) * 100

time_change = (
    (baseline_time - optimized_time)
    / baseline_time
) * 100

relevance_change = (
    (optimized_top1 - baseline_top1)
    / baseline_top1
) * 100


# ---------------------------------------------------------
# FINAL COMPARISON
# ---------------------------------------------------------
print("\n")
print("=" * 75)
print("M4.3 OPTIMIZATION COMPARISON")
print("=" * 75)

print("\nBASELINE")
print("-" * 75)
print("Top-K: 3")
print("Confidence Threshold: 0.40")
print("Domain Retrieval Accuracy:",
      round(baseline_accuracy, 2), "%")
print("Average Top-1 Relevance:",
      round(baseline_top1, 4))
print("Average Retrieved Chunks:",
      round(baseline_chunks, 2))
print("Average Response Time:",
      round(baseline_time, 2), "ms")


print("\nOPTIMIZED")
print("-" * 75)
print("Top-K: 2")
print("Confidence Threshold: 0.55")
print("Domain Retrieval Accuracy:",
      round(optimized_accuracy, 2), "%")
print("Average Top-1 Relevance:",
      round(optimized_top1, 4))
print("Average Retrieved Chunks:",
      round(optimized_chunks, 2))
print("Average Response Time:",
      round(optimized_time, 2), "ms")


print("\nIMPROVEMENT")
print("-" * 75)
print("Chunk Reduction:",
      round(chunk_reduction, 2), "%")
print("Response Time Change:",
      round(time_change, 2), "%")
print("Top-1 Relevance Change:",
      round(relevance_change, 2), "%")

print("=" * 75)
print("M4.3 BENCHMARK COMPLETED")
print("=" * 75)