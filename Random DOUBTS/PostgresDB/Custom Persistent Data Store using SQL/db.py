import os
import psycopg
from psycopg.types.json import Jsonb

from schema import SCHEMA

#  env:DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/ragdb"
DATABASE_URL = os.environ["DATABASE_URL"].replace("+psycopg", "")


def init_db():
    with psycopg.connect(DATABASE_URL) as conn:
        conn.execute(SCHEMA)


def create_conversation(user_id: str | None = None) -> str:
    with psycopg.connect(DATABASE_URL) as conn:
        row = conn.execute(
            "INSERT INTO conversations (user_id) VALUES (%s) RETURNING id",
            (user_id,),
        ).fetchone()
    return str(row[0])


def save_message(conversation_id: str, role: str, content: str, sources=None):
    with psycopg.connect(DATABASE_URL) as conn:
        conn.execute(
            "INSERT INTO messages (conversation_id, role, content, sources) "
            "VALUES (%s, %s, %s, %s)",
            (conversation_id, role, content, Jsonb(sources) if sources else None),
        )


def load_history(conversation_id: str, limit: int = 10):
    """Last `limit` messages, oldest first."""
    with psycopg.connect(DATABASE_URL) as conn:
        rows = conn.execute(
            """
            SELECT role, content FROM (
                SELECT id, role, content FROM messages
                WHERE conversation_id = %s
                ORDER BY id DESC LIMIT %s
            ) t ORDER BY id ASC
            """,
            (conversation_id, limit),
        ).fetchall()
    return rows