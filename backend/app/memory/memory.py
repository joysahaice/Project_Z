from app.database.database import get_connection


def save_memory(key: str, value: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO memory (key, value)
        VALUES (?, ?)
        ON CONFLICT(key)
        DO UPDATE SET value = excluded.value
    """, (key, value))

    conn.commit()
    conn.close()


def get_memory(key: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT value FROM memory WHERE key = ?",
        (key,)
    )

    row = cursor.fetchone()
    conn.close()

    if row:
        return row["value"]

    return None