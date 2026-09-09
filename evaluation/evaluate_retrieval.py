import sys
import os

sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "src"
    )
)

from retriever import search


test_cases = [
    {
        "id": "E1",
        "query": "What is the minimum attendance requirement?",
        "expected": "attendance_policy"
    },
    {
        "id": "E2",
        "query": "What are the examination guidelines?",
        "expected": "examination_guidelines"
    },
    {
        "id": "E3",
        "query": "How is grading calculated?",
        "expected": "grading_system"
    },
    {
        "id": "E4",
        "query": "What are the academic rules?",
        "expected": "academic_rules"
    },
    {
        "id": "T1",
        "query": "What is artificial intelligence?",
        "expected": "artificial_intelligence"
    },
    {
        "id": "T2",
        "query": "What is cloud computing?",
        "expected": "cloud_computing"
    },
    {
        "id": "T3",
        "query": "What is cybersecurity?",
        "expected": "cybersecurity_concepts"
    },
    {
        "id": "T4",
        "query": "What is machine learning?",
        "expected": "machine_learning_basics"
    }
]


top1_correct = 0
top3_correct = 0
top5_correct = 0

total = len(test_cases)

print("\n========== RETRIEVAL EVALUATION ==========\n")


for test in test_cases:

    print(f"Test ID: {test['id']}")
    print(f"Query: {test['query']}")
    print(f"Expected source: {test['expected']}")

    results = search(
        test["query"],
        top_k=5
    )

    sources = []

    for result in results:

        metadata = result.get(
            "metadata",
            {}
        )

        source = metadata.get(
            "source",
            ""
        )

        sources.append(
            source.lower()
        )

    expected = test["expected"].lower()

    top1 = any(
        expected in source
        for source in sources[:1]
    )

    top3 = any(
        expected in source
        for source in sources[:3]
    )

    top5 = any(
        expected in source
        for source in sources[:5]
    )

    if top1:
        top1_correct += 1

    if top3:
        top3_correct += 1

    if top5:
        top5_correct += 1

    print(
        "Top-1:",
        "PASS" if top1 else "FAIL"
    )

    print(
        "Top-3:",
        "PASS" if top3 else "FAIL"
    )

    print(
        "Top-5:",
        "PASS" if top5 else "FAIL"
    )

    print("Retrieved sources:")

    for source in sources:
        print("  -", source)

    print("-" * 50)


top1_accuracy = (
    top1_correct / total
) * 100

top3_accuracy = (
    top3_correct / total
) * 100

top5_accuracy = (
    top5_correct / total
) * 100


print("\n========== FINAL RESULTS ==========")

print(
    f"Top-1 Accuracy: {top1_accuracy:.2f}%"
)

print(
    f"Top-3 Accuracy: {top3_accuracy:.2f}%"
)

print(
    f"Top-5 Accuracy: {top5_accuracy:.2f}%"
)