from app.rag.vector_store import get_vector_store


def search_documents(query: str, k: int = 5):
    vector_store = get_vector_store()

    docs = vector_store.similarity_search(query, k=k)

    context = ""

    sources = []

    for doc in docs:
        context += doc.page_content + "\n\n"

        source = doc.metadata.get("source", "Unknown")

        if source not in sources:
            sources.append(source)

    return {
        "context": context,
        "sources": sources,
    }