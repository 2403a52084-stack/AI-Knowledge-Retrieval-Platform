from src.agents.orchestrator import Orchestrator


# ============================================================
# MILESTONE 4.2 - ISOLATED END-TO-END TESTING
# ============================================================

def run_independent_test(
    test_number,
    domain,
    question
):

    # Create a fresh orchestrator for every independent test.
    # This prevents previous conversation memory from
    # contaminating the next domain test.

    orchestrator = Orchestrator()

    result = orchestrator.process_query(
        question
    )

    print("\n" + "=" * 70)
    print(f"TEST {test_number} - {domain}")
    print("=" * 70)

    print(
        "Question:",
        question
    )

    print(
        "Status:",
        result.get("status")
    )

    classification = result.get(
        "classification",
        {}
    )

    print(
        "Query Type:",
        classification.get(
            "query_type"
        )
    )

    print(
        "Routing:",
        classification.get(
            "routing"
        )
    )

    print(
        "Confidence:",
        result.get(
            "confidence"
        )
    )

    print(
        "Confidence Score:",
        result.get(
            "confidence_score"
        )
    )

    retrieval = result.get(
        "retrieval",
        {}
    )

    retrieved_results = retrieval.get(
        "results",
        []
    )

    print(
        "Retrieved Chunks:",
        len(retrieved_results)
    )

    correct_domain = False

    for item in retrieved_results:

        metadata = item.get(
            "metadata",
            {}
        )

        source = metadata.get(
            "source",
            metadata.get(
                "filename",
                "Unknown"
            )
        )

        retrieved_domain = str(
            metadata.get(
                "domain",
                "Unknown"
            )
        ).lower()

        relevance = item.get(
            "relevance_score"
        )

        print(
            "Source:",
            source
        )

        print(
            "Domain:",
            retrieved_domain
        )

        print(
            "Relevance:",
            relevance
        )

        if retrieved_domain == domain.lower():

            correct_domain = True


    # --------------------------------------------------------
    # CHECK RESULT
    # --------------------------------------------------------

    passed = (
        result.get("status") == "success"
        and correct_domain
    )

    print(
        "Domain Retrieval Check:",
        "PASS" if passed else "FAIL"
    )

    return passed


# ============================================================
# TEST 1 - EDUCATION
# ============================================================

education_pass = run_independent_test(
    1,
    "education",
    "What is the minimum attendance percentage required?"
)


# ============================================================
# TEST 2 - TECHNOLOGY
# ============================================================

technology_pass = run_independent_test(
    2,
    "technology",
    "What is cloud computing?"
)


# ============================================================
# TEST 3 - FINANCE
# ============================================================

finance_pass = run_independent_test(
    3,
    "finance",
    "What is a savings account?"
)


# ============================================================
# TEST 4 - FINANCE COMPARATIVE
# ============================================================

comparative_pass = run_independent_test(
    4,
    "finance",
    "What is the difference between a savings account and a fixed deposit?"
)


# ============================================================
# TEST 5 - AMBIGUOUS QUERY
# ============================================================

ambiguous_orchestrator = Orchestrator()

ambiguous_query = "Finance"

ambiguous_result = (
    ambiguous_orchestrator.process_query(
        ambiguous_query
    )
)

print("\n" + "=" * 70)
print("TEST 5 - AMBIGUOUS QUERY")
print("=" * 70)

print(
    "Question:",
    ambiguous_query
)

print(
    "Status:",
    ambiguous_result.get(
        "status"
    )
)

print(
    "Expected:",
    "clarification_required"
)

ambiguous_pass = (
    ambiguous_result.get(
        "status"
    )
    == "clarification_required"
)

print(
    "Ambiguous Test:",
    "PASS" if ambiguous_pass else "FAIL"
)


# ============================================================
# TEST 6 - MEMORY TEST
# ============================================================

memory_orchestrator = Orchestrator()


memory_q1 = (
    "What is cloud computing?"
)

memory_r1 = (
    memory_orchestrator.process_query(
        memory_q1
    )
)


memory_q2 = (
    "What are its services?"
)

memory_r2 = (
    memory_orchestrator.process_query(
        memory_q2
    )
)


print("\n" + "=" * 70)
print("TEST 6 - CONVERSATION MEMORY")
print("=" * 70)

print(
    "Turn 1:",
    memory_q1
)

print(
    "Turn 1 Status:",
    memory_r1.get(
        "status"
    )
)

print(
    "Turn 2:",
    memory_q2
)

print(
    "Turn 2 Status:",
    memory_r2.get(
        "status"
    )
)

print(
    "Turn 2 Answer:",
    memory_r2.get(
        "answer"
    )
)

memory_pass = (
    memory_r1.get("status") == "success"
    and memory_r2.get("status") == "success"
)

print(
    "Memory Test:",
    "PASS" if memory_pass else "FAIL"
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("MILESTONE 4.2 FINAL SUMMARY")
print("=" * 70)

results = {
    "Education": education_pass,
    "Technology": technology_pass,
    "Finance": finance_pass,
    "Comparative Finance": comparative_pass,
    "Ambiguous Query": ambiguous_pass,
    "Conversation Memory": memory_pass
}

for name, passed in results.items():

    print(
        f"{name:<25} -> "
        f"{'PASS' if passed else 'FAIL'}"
    )


total_passed = sum(
    results.values()
)

total_tests = len(
    results
)

print(
    f"\nPassed: {total_passed}/{total_tests}"
)

print("=" * 70)