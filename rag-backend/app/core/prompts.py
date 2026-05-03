def build_rag_prompt(context: str, question: str) -> str:
    return f"""
You are a helpful assistant.
Answer the question using only the context below.

If the answer is not in the context, say:
"I don't know based on the provided context."

Context:
{context}

Question:
{question}

Answer:
"""