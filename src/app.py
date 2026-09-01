import streamlit as st

from retriever import search
from answer_generator import generate_answer


st.set_page_config(
    page_title="AI Knowledge Retrieval Platform",
    page_icon="🤖"
)

st.title("🤖 AI Knowledge Retrieval Platform")
st.write("Ask questions about the documents in the knowledge base.")


question = st.text_input("Enter your question:")


if st.button("Ask Question"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        results = search(question, top_k=3)

        context_parts = []

        for result in results:

            if isinstance(result, dict):
                text = result.get("text", "")
            else:
                text = str(result)

            if text:
                context_parts.append(text)

        context = "\n\n".join(context_parts)

        answer = generate_answer(
            question,
            context
        )

        st.subheader("Answer")
        st.success(answer)
        