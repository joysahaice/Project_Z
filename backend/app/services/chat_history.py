from app.database.database import get_connection


def save_chat(role: str, message: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO chats(role, message) VALUES(?, ?)",
        (role, message)
    )

    conn.commit()
    conn.close()


def get_last_messages(limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role, message
        FROM chats
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return list(reversed(rows))