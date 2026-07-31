from app.rag.search import search_documents


PDF_KEYWORDS = [
    "pdf",
    "document",
    "file",
    "paper",
    "chapter",
    "page",
    "according to",
    "from the pdf",
]


def should_use_rag(message: str) -> bool:
    message = message.lower()

    return any(keyword in message for keyword in PDF_KEYWORDS)


def get_rag_context(message: str) -> str:
    return search_documents(message)