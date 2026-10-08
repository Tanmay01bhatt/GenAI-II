# $env:REDIS_URL="redis://localhost:6379/0"
import os
import json
import hashlib
import redis

r = redis.Redis.from_url(
    os.environ.get("REDIS_URL", "redis://localhost:6379/0"),
    decode_responses=True,
)

ANSWER_TTL = 60 * 60 * 24    # 24 hours
KB_VERSION = "v1"            # bump when you re-ingest documents


def _key(question: str) -> str:
    normalized = " ".join(question.lower().split())   # ignore case/extra spaces
    digest = hashlib.sha256(normalized.encode()).hexdigest()
    return f"answer:{KB_VERSION}:{digest}"


def get_cached_answer(question: str) -> dict | None:
    data = r.get(_key(question))
    return json.loads(data) if data else None   # {"answer": ..., "sources": [...]}


def set_cached_answer(question: str, answer: str, sources: list) -> None:
    r.set(_key(question), json.dumps({"answer": answer, "sources": sources}), ex=ANSWER_TTL)