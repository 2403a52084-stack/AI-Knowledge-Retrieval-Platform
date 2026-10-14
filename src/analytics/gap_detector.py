import json
from collections import Counter

from .analytics_store import get_all_analytics


# ============================================================
# KNOWLEDGE GAP DETECTOR
# ============================================================

def detect_knowledge_gaps(
    confidence_threshold=0.50,
    repeat_threshold=2
):
    """
    Detect repeated or low-confidence queries that may
    represent gaps in the knowledge base.
    """

    records = get_all_analytics()

    gaps = []

    # --------------------------------------------------------
    # Find low-confidence / unresolved queries
    # --------------------------------------------------------

    candidate_queries = []

    for record in records:

        status = record.get("status")

        confidence_score = record.get(
            "confidence_score"
        )

        query = str(
            record.get("query", "")
        ).strip()


        low_confidence = (
            confidence_score is not None
            and confidence_score < confidence_threshold
        )

        unresolved = status in [
            "low_confidence",
            "no_results",
            "clarification_required",
            "error"
        ]


        if query and (
            low_confidence or unresolved
        ):

            candidate_queries.append(
                query.lower()
            )


    # --------------------------------------------------------
    # Count repeated questions
    # --------------------------------------------------------

    query_counts = Counter(
        candidate_queries
    )


    # --------------------------------------------------------
    # Create gap report
    # --------------------------------------------------------

    for query, count in query_counts.items():

        if count >= repeat_threshold:

            gaps.append({
                "query": query,
                "occurrences": count,
                "reason": (
                    "Repeated low-confidence or "
                    "unresolved query"
                )
            })


    return gaps


# ============================================================
# LOW CONFIDENCE REPORT
# ============================================================

def get_low_confidence_report(
    threshold=0.50
):
    """
    Return low-confidence interactions.
    """

    records = get_all_analytics()

    report = []

    for record in records:

        score = record.get(
            "confidence_score"
        )

        if (
            score is not None
            and score < threshold
        ):

            report.append(record)


    return report


# ============================================================
# DOMAIN ANALYSIS
# ============================================================

def get_domain_summary():
    """
    Count queries by domain.
    """

    records = get_all_analytics()

    domain_counts = Counter()

    for record in records:

        domain = record.get(
            "domain",
            "Unknown"
        )

        domain_counts[domain] += 1

    return dict(
        domain_counts
    )


# ============================================================
# QUERY TYPE ANALYSIS
# ============================================================

def get_query_type_summary():
    """
    Count queries by query type.
    """

    records = get_all_analytics()

    type_counts = Counter()

    for record in records:

        query_type = record.get(
            "query_type",
            "Unknown"
        )

        type_counts[query_type] += 1

    return dict(
        type_counts
    )


# ============================================================
# STATUS ANALYSIS
# ============================================================

def get_status_summary():
    """
    Count queries by resolution status.
    """

    records = get_all_analytics()

    status_counts = Counter()

    for record in records:

        status = record.get(
            "status",
            "Unknown"
        )

        status_counts[status] += 1

    return dict(
        status_counts
    )


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("KNOWLEDGE GAP DETECTION")
    print("=" * 60)

    print("\nKnowledge gaps:")

    gaps = detect_knowledge_gaps()

    if gaps:

        for gap in gaps:
            print(gap)

    else:

        print(
            "No repeated knowledge gaps detected."
        )


    print("\nDomain summary:")
    print(
        get_domain_summary()
    )


    print("\nQuery type summary:")
    print(
        get_query_type_summary()
    )


    print("\nStatus summary:")
    print(
        get_status_summary()
    )