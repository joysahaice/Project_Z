memory = {}


def save_memory(key: str, value: str):
    memory[key] = value


def get_memory(key: str):
    return memory.get(key)