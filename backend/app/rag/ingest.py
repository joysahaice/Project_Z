import os

from langchain_core.documents import Document

from app.rag.pdf_loader import load_pdf
from app.rag.text_splitter import split_text
from app.rag.vector_store import get_vector_store


def ingest_pdf(
    file_path: str,
    original_filename: str
):
    pages = load_pdf(file_path)

    filename = original_filename

    documents = []

    for page in pages:
        page_number = page["page"]
        page_text = page["text"]

        chunks = split_text(page_text)

        for chunk in chunks:
            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "source": filename,
                        "page": page_number,
                    },
                )
            )

    vector_store = get_vector_store()

    vector_store.add_documents(documents)

    return len(documents)