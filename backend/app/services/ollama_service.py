from click import prompt
import httpx

from app.memory.memory import save_memory, get_memory
from app.services.chat_history import save_chat, get_last_messages
from app.rag.search import search_documents
from app.services.router import should_use_rag, get_rag_context

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


async def generate_response(prompt: str) -> str:
    lower = prompt.lower()

    # Save user message
    save_chat("user", prompt)

    # Save user's name
    if lower.startswith("my name is "):
        name = prompt[11:].strip()
        save_memory("name", name)

        reply = f"Nice to meet you, {name}! I'll remember your name."
        save_chat("assistant", reply)
        return reply

    # Save user's name (alternative)
    if lower.startswith("i am "):
        name = prompt[5:].strip()
        save_memory("name", name)

        reply = f"Nice to meet you, {name}! I'll remember your name."
        save_chat("assistant", reply)
        return reply

    # Recall user's name
    if "what is my name" in lower:
        name = get_memory("name")

        if name:
            reply = f"Your name is {name}."
        else:
            reply = "I don't know your name yet."

        save_chat("assistant", reply)
        return reply
    history = get_last_messages(10)

    rag_context = ""

    if should_use_rag(prompt):
        rag_context = get_rag_context(prompt)

    context = ""

    for msg in history:
        context += f"{msg['role']}: {msg['message']}\n"

    full_prompt = f"""
    You are Project Z, a helpful personal AI assistant.

    Previous conversation:
    {context}

    Relevant document context:
    {rag_context}

    Current user message:
    {prompt}

    Instructions:
    - If relevant document context exists, answer using it.
    - Otherwise answer normally.

    Assistant:
    """

    # Send request to Ollama
    payload = {
        "model": "qwen2.5:3b",
        "prompt": full_prompt,
        "stream": False,
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(OLLAMA_URL, json=payload)
        response.raise_for_status()

        data = response.json()
        reply = data["response"]

        save_chat("assistant", reply)

        return reply