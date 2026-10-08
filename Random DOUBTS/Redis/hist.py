# $env:REDIS_URL="redis://localhost:6379/0"

import os
import json
import hashlib
import redis

r = redis.Redis.from_url(
    os.environ.get("REDIS_URL", "redis://localhost:6379/0"),
    decode_responses=True,          # return str instead of bytes
)

HISTORY_TTL = 60 * 60               # 1 hour
ANSWER_TTL = 60 * 60 * 24           # 24 hours
KB_VERSION = "v1"                   # bump when you re-ingest documents


def _hist_key(conversation_id: str) -> str:
    return f"chat:{conversation_id}:history"


def get_history(conversation_id: str, limit: int = 10):
    """Returns [(role, content), ...] oldest first, or [] if not cached."""
    items = r.lrange(_hist_key(conversation_id), -limit, -1)
    return [tuple(json.loads(i)) for i in items]


def push_message(conversation_id: str, role: str, content: str):
    key = _hist_key(conversation_id)
    r.rpush(key, json.dumps([role, content]))   # append to a Redis list
    r.ltrim(key, -50, -1)                       # keep only the last 50
    r.expire(key, HISTORY_TTL)                  # reset expiry


def warm_history(conversation_id: str, rows):
    """Fill the cache from Postgres rows."""
    for role, content in rows:
        push_message(conversation_id, role, content)

'''

rpush: add an item to the end of a list.
lrange(key, -10, -1): read the last 10 items.
ltrim: cut the list down so it doesn’t grow forever.
expire / ex=: auto-delete the key after N seconds.
get / set: plain key and value.

'''