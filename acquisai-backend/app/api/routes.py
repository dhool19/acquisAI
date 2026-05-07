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

def is_small_talk(question: str) -> bool:
    q = question.lower().strip()

    small_talk = {
        "hi", "hello", "hey",
        "good morning", "good evening",
        "thanks", "thank you", "bye"
    }

    return q in small_talk

@router.post("/ask")
def ask_question(request: QuestionRequest):
    question = request.question.strip()

    # 1. Handle small talk WITHOUT RAG
    if is_small_talk(question):
        return {
            "question": question,
            "context": "",
            "answer": "Hello! How can I help you?",
            "sources": [],
        }

    # 2. Normal RAG flow
    retrieved_chunks = retrieve_context(question)

    # Optional safety: no useful chunks
    if not retrieved_chunks:
        return {
            "question": question,
            "context": "",
            "answer": "I don't have enough information in the documents to answer that.",
            "sources": [],
        }

    context_text = "\n\n".join(
        f"[Source: {chunk['file_name']}, Page: {chunk['page_number']}]\n{chunk['text']}"
        for chunk in retrieved_chunks
    )

    prompt = build_rag_prompt(
        context=context_text,
        question=question
    )

    answer = generate_answer(prompt)

    sources = format_sources(retrieved_chunks)

    return {
        "question": question,
        "context": context_text,
        "answer": answer,
        "sources": sources,
    }