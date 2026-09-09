from answer_generator import generate_answer


class ResponseGenerationAgent:
    """
    Generates the final answer using retrieved context.
    """

    def generate(self, query, results):

        context_parts = []

        for result in results:
            text = result.get("text", "")

            if text:
                context_parts.append(text)

        context = "\n\n".join(context_parts)

        return generate_answer(
            query,
            context
        )
