import httpx


OLLAMA_URL = "http://localhost:11434/api/generate"


async def generate_response(prompt: str) -> str:
    payload = {
        "model": "qwen2.5:3b",
        "prompt": prompt,
        "stream": False
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(OLLAMA_URL, json=payload)
        response.raise_for_status()

        data = response.json()
        return data["response"]