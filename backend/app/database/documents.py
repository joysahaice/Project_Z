from app.database.database import get_connection


def add_document(filename: str, chunks: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO documents (filename, chunks)
        VALUES (?, ?)
        """,
        (filename, chunks),
    )

    conn.commit()
    conn.close()


def get_documents():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            filename,
            chunks,
            upload_time
        FROM documents
        ORDER BY upload_time DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_document_by_id(document_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM documents
        WHERE id = ?
        """,
        (document_id,),
    )

    row = cursor.fetchone()

    conn.close()

    return row


def document_exists(filename: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM documents
        WHERE filename = ?
        """,
        (filename,),
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None


def delete_document(document_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM documents
        WHERE id = ?
        """,
        (document_id,),
    )

    conn.commit()
    conn.close()