from langchain_core.documents import Document

from app.rag.pdf_loader import load_pdf
from app.rag.text_splitter import split_text
from app.rag.vector_store import get_vector_store


def ingest_pdf(file_path: str):
    text = load_pdf(file_path)

    chunks = split_text(text)

    documents = [
        Document(page_content=chunk)
        for chunk in chunks
    ]

    vector_store = get_vector_store()

    vector_store.add_documents(documents)

    return len(documents)