from fastapi import FastAPI
from app.models.chat import ChatRequest, ChatResponse
from app.services.ollama_service import generate_response

app = FastAPI(
    title="Project Z API",
    description="Personal AI Assistant Backend",
    version="0.1.0"
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