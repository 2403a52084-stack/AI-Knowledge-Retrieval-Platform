from retriever import search
from answer_generator import generate_answer


def main():

    print("=" * 60)
    print("AI KNOWLEDGE RETRIEVAL SYSTEM")
    print("=" * 60)

    print("\nType 'exit' to stop the program.")

    while True:

        query = input("\nEnter your question: ")

        # Stop the program
        if query.lower().strip() == "exit":
            print("\nGoodbye!")
            break

        # Ignore empty questions
        if not query.strip():
            print("Please enter a question.")
            continue

        # Retrieve relevant documents
        results = search(query, top_k=3)

        # Build context
        context_parts = []

        for result in results:

            if isinstance(result, dict):
                text = result.get("text", "")
            else:
                text = str(result)

            if text:
                context_parts.append(text)

        context = "\n\n".join(context_parts)

        # Generate answer
        answer = generate_answer(query, context)

        print("\n" + "=" * 60)
        print("FINAL ANSWER")
        print("=" * 60)

        print(answer)


if __name__ == "__main__":
    main()