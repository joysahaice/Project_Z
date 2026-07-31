from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

DB_PATH = "vector_db"


def get_vector_store():
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    return Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )