class ResponseGenerationAgent:

    def __init__(self):
        pass

    def process_query(self, query, retrieval_result):
        """
        Generate a grounded response using only retrieved knowledge-base content.
        """

        query = str(query).strip()

        if not query:
            return {
                "query": query,
                "answer": "No question was provided.",
                "confidence": "Low",
                "confidence_score": 0.0,
                "sources": [],
                "status": "error"
            }

        if not retrieval_result:
            return {
                "query": query,
                "answer": (
                    "I could not find sufficiently relevant information "
                    "in the knowledge base."
                ),
                "confidence": "Low",
                "confidence_score": 0.0,
                "sources": [],
                "status": "no_results"
            }

        status = retrieval_result.get("status", "")

        if status != "success":
            return {
                "query": query,
                "answer": retrieval_result.get(
                    "message",
                    "No sufficiently relevant information was found."
                ),
                "confidence": "Low",
                "confidence_score": 0.0,
                "sources": [],
                "status": status
            }

        results = retrieval_result.get("results", [])

        if not results:
            return {
                "query": query,
                "answer": (
                    "I could not find enough supporting information "
                    "in the knowledge base."
                ),
                "confidence": "Low",
                "confidence_score": 0.0,
                "sources": [],
                "status": "no_results"
            }

        # Use only retrieved chunks as evidence
        context_parts = []

        for item in results:
            text = item.get("text", "").strip()

            if text:
                context_parts.append(text)

        if not context_parts:
            return {
                "query": query,
                "answer": (
                    "The knowledge base did not provide enough evidence "
                    "to answer this question."
                ),
                "confidence": "Low",
                "confidence_score": 0.0,
                "sources": [],
                "status": "no_evidence"
            }

        # Calculate application-level confidence
        scores = [
            float(item.get("relevance_score", 0.0))
            for item in results
            if item.get("relevance_score") is not None
        ]

        if scores:
            confidence_score = max(scores)
        else:
            confidence_score = 0.0

        if confidence_score >= 0.70:
            confidence = "High"
        elif confidence_score >= 0.50:
            confidence = "Medium"
        else:
            confidence = "Low"

        # Simple grounded response construction
        if len(context_parts) == 1:
            answer = context_parts[0]
        else:
            answer = " ".join(context_parts)

        # Source attribution
        sources = []

        for item in results:
            metadata = item.get("metadata", {}) or {}

            source = (
                item.get("source")
                or metadata.get("source")
                or metadata.get("filename")
                or "Unknown"
            )

            page = (
                item.get("page")
                or metadata.get("page")
                or metadata.get("page_number")
            )

            chunk_id = (
                item.get("chunk_id")
                or metadata.get("chunk_id")
                or metadata.get("chunk_index")
            )

            sources.append({
                "source": source,
                "page": page,
                "chunk_id": chunk_id,
                "relevance_score": item.get("relevance_score", 0.0)
            })

        return {
            "query": query,
            "answer": answer,
            "confidence": confidence,
            "confidence_score": round(confidence_score, 4),
            "sources": sources,
            "status": "success"
        }