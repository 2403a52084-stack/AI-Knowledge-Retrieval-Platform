from src.retriever import retrieve


class RetrievalAgent:

    def __init__(self, top_k=3, confidence_threshold=0.60):
        self.top_k = top_k
        self.confidence_threshold = confidence_threshold

    def process_query(self, query, query_type="factual", top_k=None):

        query = str(query).strip()

        if not query:
            return {
                "query": query,
                "query_type": query_type,
                "results": [],
                "status": "no_results",
                "message": "No query was provided."
            }

        if query_type == "ambiguous":
            return {
                "query": query,
                "query_type": query_type,
                "results": [],
                "status": "clarification_required",
                "message": "The query is ambiguous and requires clarification."
            }

        k = top_k if top_k is not None else self.top_k

        try:
            raw_results = retrieve(query, top_k=k)

            if not raw_results:
                return {
                    "query": query,
                    "query_type": query_type,
                    "results": [],
                    "status": "no_results",
                    "message": "No relevant information was found."
                }

            processed = []

            for item in raw_results:

                metadata = item.get("metadata", {}) or {}
                distance = item.get("distance")

                try:
                    distance = float(distance)
                except (TypeError, ValueError):
                    distance = None

                if distance is not None:
                    relevance_score = 1.0 / (1.0 + max(distance, 0.0))
                else:
                    relevance_score = 0.0

                processed.append({
                    "text": item.get("text", ""),
                    "metadata": metadata,
                    "source": metadata.get("source", "Unknown"),
                    "chunk_id": metadata.get(
                        "chunk_id",
                        metadata.get("chunk_index", "Unknown")
                    ),
                    "page": metadata.get(
                        "page",
                        metadata.get("page_number", "Unknown")
                    ),
                    "distance": distance,
                    "relevance_score": round(
                        relevance_score, 4
                    )
                })

            processed.sort(
                key=lambda x: x["relevance_score"],
                reverse=True
            )

            filtered = [
                item
                for item in processed
                if item["relevance_score"] >= self.confidence_threshold
            ]

            if not filtered:
                return {
                    "query": query,
                    "query_type": query_type,
                    "results": [],
                    "status": "low_confidence",
                    "message": (
                        "No sufficiently relevant information "
                        "was found in the knowledge base."
                    )
                }

            for rank, item in enumerate(filtered, start=1):
                item["rank"] = rank

            return {
                "query": query,
                "query_type": query_type,
                "top_k": k,
                "results": filtered,
                "status": "success",
                "message": (
                    f"{len(filtered)} relevant result(s) retrieved."
                )
            }

        except Exception as error:

            return {
                "query": query,
                "query_type": query_type,
                "results": [],
                "status": "error",
                "message": f"Retrieval failed: {error}"
            }