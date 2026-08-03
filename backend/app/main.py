from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.chat import ChatRequest, ChatResponse
from app.services.ollama_service import generate_response
from app.database.database import init_database
from fastapi import UploadFile, File
from app.models.pdf import PDFResponse
from app.rag.ingest import ingest_pdf
from app.rag.vector_store import delete_document_vectors
from app.database.documents import (
    add_document,
    get_documents,
    document_exists,
    get_document_by_id,
    delete_document,
)
from app.models.document import DocumentResponse
import tempfile
import os



app = FastAPI(
    title="Project Z API",
    description="Personal AI Assistant Backend",
    version="0.1.0"
)

init_database()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to Project Z 🚀"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    reply = await generate_response(request.message)
    return ChatResponse(reply=reply)
@app.post("/upload-pdf", response_model=PDFResponse)
async def upload_pdf(file: UploadFile = File(...)):

    if document_exists(file.filename):
        return PDFResponse(
            status="error",
            chunks=0,
            message="Document already exists."
        )

    suffix = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
        temp.write(await file.read())
        temp_path = temp.name

    chunks = ingest_pdf(
        temp_path,
        original_filename=file.filename
    )

    add_document(
        filename=file.filename,
        chunks=chunks
    )

    os.remove(temp_path)

    return PDFResponse(
        status="success",
        chunks=chunks,
        message="Document uploaded successfully."
    )
@app.get("/documents", response_model=list[DocumentResponse])
async def list_documents():
    rows = get_documents()

    return [
        DocumentResponse(
            id=row["id"],
            filename=row["filename"],
            chunks=row["chunks"],
            upload_time=row["upload_time"],
        )
        for row in rows
    ]

@app.delete("/documents/{document_id}")
async def remove_document(document_id: int):

    document = get_document_by_id(document_id)

    if document is None:
        return {
            "status": "error",
            "message": "Document not found."
        }
    delete_document_vectors(document["filename"])

    delete_document(document_id)

    return {
        "status": "success",
        "message": "Document deleted successfully."
    }