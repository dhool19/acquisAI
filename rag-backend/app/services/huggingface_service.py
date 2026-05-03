from transformers import pipeline
from app.core.config import HF_MODEL_NAME

generator = pipeline(
    "text2text-generation",
    model=HF_MODEL_NAME
)

def generate_answer(question: str, context: str) -> str:
    prompt = f"""
Answer the question using the context.

Context:
{context}

Question:
{question}

Answer:
"""

    response = generator(
        prompt,
        max_new_tokens=80,
        do_sample=False
    )

    return response[0]["generated_text"].strip()