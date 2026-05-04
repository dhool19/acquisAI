from fastapi import APIRouter
from pydantic import BaseModel

from app.core.prompts import build_rag_prompt
from app.services.openai_service import generate_answer
from app.services.retriever import retrieve_context

router = APIRouter()


class QuestionRequest(BaseModel):
    question: str

def format_sources(chunks):
    grouped = {}

    for chunk in chunks:
        file_name = chunk.get("file_name", "unknown")
        page = chunk.get("page_number", None)

        if file_name not in grouped:
            grouped[file_name] = set()

        if page:
            grouped[file_name].add(page)

    formatted = []
    for file_name, pages in grouped.items():
        formatted.append({
            "file_name": file_name,
            "pages": sorted(list(pages))
        })

    return formatted

@router.post("/ask")
def ask_question(request: QuestionRequest):
    retrieved_chunks = retrieve_context(request.question)

    context_text = "\n\n".join(
        f"[Source: {chunk['file_name']}, Page: {chunk['page_number']}]\n{chunk['text']}"
        for chunk in retrieved_chunks
    )

    prompt = build_rag_prompt(
        context=context_text,
        question=request.question
    )

    answer = generate_answer(prompt)

    sources = format_sources(retrieved_chunks)

    return {
        "question": request.question,
        "context": context_text,
        "answer": answer,
        "sources": sources,
    }