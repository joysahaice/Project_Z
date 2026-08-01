from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.chat import ChatRequest, ChatResponse
from app.services.ollama_service import generate_response
from app.database.database import init_database
from fastapi import UploadFile, File
import fitz
from app.models.pdf import PDFResponse
from app.rag.ingest import ingest_pdf
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
    suffix = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
        temp.write(await file.read())
        temp_path = temp.name

    chunks = ingest_pdf(
    temp_path,
    original_filename=file.filename
)

    os.remove(temp_path)

    return PDFResponse(
        status="success",
        chunks=chunks
    )