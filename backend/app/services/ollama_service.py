import httpx
from app.memory.memory import save_memory, get_memory

OLLAMA_URL = "http://localhost:11434/api/generate"


async def generate_response(prompt: str) -> str:

    lower = prompt.lower()

    # Save user's name
    if lower.startswith("my name is "):
        name = prompt[11:].strip()
        save_memory("name", name)
        return f"Nice to meet you, {name}! I'll remember your name."

    if lower.startswith("i am "):
        name = prompt[5:].strip()
        save_memory("name", name)
        return f"Nice to meet you, {name}! I'll remember your name."

    # Recall name
    if "what is my name" in lower:
        name = get_memory("name")
        if name:
            return f"Your name is {name}."
        else:
            return "I don't know your name yet."

    payload = {
        "model": "qwen2.5:3b",
        "prompt": prompt,
        "stream": False,
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(OLLAMA_URL, json=payload)
        response.raise_for_status()

        data = response.json()
        return data["response"]