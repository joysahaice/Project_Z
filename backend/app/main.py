from fastapi import FastAPI

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