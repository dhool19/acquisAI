def build_rag_prompt(context: str, question: str) -> str:
    return f"""
You are a helpful assistant.

Use the provided context to answer the question.

Rules:
1. If the answer is clearly in the context, answer ONLY from the context.
2. Do NOT add outside knowledge when context is sufficient.
3. If the question is conceptual, relate it strictly to the context.
4. If the answer is not in the context, say:
   "I don't know based on the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""