from app.rag.vector_store import get_vector_store


def search_documents(query: str, k: int = 5):
    vector_store = get_vector_store()

    docs = vector_store.similarity_search(query, k=k)

    context = "\n\n".join(doc.page_content for doc in docs)

    return context