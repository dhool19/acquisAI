from openai import OpenAI

from app.core.config import OPENAI_API_KEY, OPENAI_MODEL_NAME

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_answer(prompt: str) -> str:
    response = client.chat.completions.create(
        model=OPENAI_MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You answer using retrieved context only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content