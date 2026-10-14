from .analytics_store import save_query_analytics


def track_query(
    query,
    query_type=None,
    routing=None,
    status=None,
    confidence=None,
    confidence_score=None,
    clarification_required=False,
    response_time_ms=None,
    domain=None,
    retrieved_sources=None
):
    """
    Track one real application query in the analytics database.
    """

    save_query_analytics(
        query=query,
        query_type=query_type,
        routing=routing,
        status=status,
        confidence=confidence,
        confidence_score=confidence_score,
        clarification_required=clarification_required,
        response_time_ms=response_time_ms,
        domain=domain,
        retrieved_sources=retrieved_sources
    )

    return True