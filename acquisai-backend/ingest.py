import os
import chromadb
import pdfplumber
from sentence_transformers import SentenceTransformer

from app.core.config import (
    DATA_PATH,
    CHROMA_DB_PATH,
    COLLECTION_NAME,
    EMBEDDING_MODEL_NAME,
)

model = SentenceTransformer(EMBEDDING_MODEL_NAME)

client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)


def clean_text(text: str) -> str:
    clean_lines = []

    for line in text.split("\n"):
        line = line.strip()

        if not line:
            continue

        if "OJ L" in line:
            continue

        if "Special edition" in line:
            continue

        clean_lines.append(line)

    return "\n\n".join(clean_lines)


def load_pdf_pages(path: str):
    pages = []

    with pdfplumber.open(path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text()

            if page_text and page_text.strip():
                pages.append(
                    {
                        "page_number": page_number,
                        "text": page_text.strip(),
                    }
                )

    return pages


def chunk_text(text: str, chunk_size: int = 700):
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()

        if not paragraph:
            continue

        if len(current_chunk) + len(paragraph) <= chunk_size:
            current_chunk += "\n\n" + paragraph
        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())

            current_chunk = paragraph

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


def get_pdf_files(data_dir: str):
    return [
        os.path.join(data_dir, file)
        for file in os.listdir(data_dir)
        if file.lower().endswith(".pdf")
    ]


def ingest():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"{DATA_PATH} folder not found")

    pdf_files = get_pdf_files(DATA_PATH)

    if not pdf_files:
        raise FileNotFoundError("No PDF files found in data folder")

    total_chunks = 0

    for pdf_path in pdf_files:
        print(f"Reading {pdf_path}...")

        pages = load_pdf_pages(pdf_path)

        if not pages:
            print(f"Skipped {pdf_path}, no text extracted")
            continue

        file_name = os.path.basename(pdf_path)
        file_chunk_count = 0

        for page in pages:
            page_number = page["page_number"]

            text = clean_text(page["text"])

            if not text:
                continue

            chunks = chunk_text(text)

            for chunk_index, chunk in enumerate(chunks):
                embedding = model.encode(chunk).tolist()

                chunk_id = f"{file_name}_page_{page_number}_chunk_{chunk_index}"

                collection.upsert(
                    ids=[chunk_id],
                    documents=[chunk],
                    embeddings=[embedding],
                    metadatas=[
                        {
                            "source": pdf_path,
                            "file_name": file_name,
                            "page_number": page_number,
                            "chunk_index": chunk_index,
                        }
                    ],
                )

            file_chunk_count += len(chunks)

        total_chunks += file_chunk_count
        print(f"Ingested {file_chunk_count} chunks from {file_name}")

    print(f"Total ingested chunks: {total_chunks}")


if __name__ == "__main__":
    ingest()