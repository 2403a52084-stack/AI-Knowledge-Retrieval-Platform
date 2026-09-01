from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


MODEL_NAME = "google/flan-t5-small"


print("Loading answer generation model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


def generate_answer(question, context):

    prompt = f"""
Context:
{context}

Question:
{question}

Answer the question using the context.
Give a complete sentence.

Question: What is phishing?
Answer: Phishing is a social engineering attack that attempts to obtain sensitive information.

Question: What is cloud computing?
Answer: Cloud computing provides computing resources through network-accessible services.

Question: What is machine learning?
Answer: Machine learning is a branch of artificial intelligence that enables computers to learn patterns from data.

Now answer this question:

Question: {question}
Answer:
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=80,
        do_sample=False
    )

    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    ).strip()

    return answer


if __name__ == "__main__":

    question = input("Question: ")

    context = """
    Phishing is a social engineering attack that attempts to obtain
    sensitive information.
    """

    answer = generate_answer(
        question,
        context
    )

    print("\nAnswer:")
    print(answer)