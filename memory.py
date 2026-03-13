"""
memory.py — Persistent vector memory using ChromaDB.
Stores every conversation turn and retrieves semantically similar past context.
"""
import hashlib
from datetime import datetime
import chromadb
from config import CHROMA_DIR, MEMORY_RESULTS
from logger import get_logger

log = get_logger("memory")

_client = chromadb.PersistentClient(path=CHROMA_DIR)
_col    = _client.get_or_create_collection(
    name="bujji_memory",
    metadata={"hnsw:space": "cosine"},
)


def _uid(text: str) -> str:
    ts = datetime.now().isoformat(timespec="microseconds")
    return hashlib.md5(f"{text}{ts}".encode()).hexdigest()[:14]


def save_memory(user_input: str, response: str, emotion: str = "neutral"):
    try:
        doc = f"User: {user_input}\nBUJJI: {response}"
        _col.add(
            documents=[doc],
            ids=[_uid(doc)],
            metadatas=[{
                "timestamp": datetime.now().isoformat(),
                "emotion":   emotion,
                "user_input": user_input[:200],
            }],
        )
        log.debug(f"Saved memory — {user_input[:50]}")
    except Exception as e:
        log.warning(f"Memory save failed: {e}")


def get_relevant_memory(query: str, n: int = MEMORY_RESULTS) -> str:
    try:
        count = _col.count()
        if count == 0:
            return ""
        results = _col.query(query_texts=[query], n_results=min(n, count))
        docs = results.get("documents", [[]])[0]
        return "\n---\n".join(docs) if docs else ""
    except Exception as e:
        log.warning(f"Memory query failed: {e}")
        return ""


def clear_memory() -> str:
    try:
        ids = _col.get()["ids"]
        if ids:
            _col.delete(ids=ids)
        log.info(f"Memory cleared ({len(ids)} entries)")
        return f"Memory cleared. {len(ids)} interactions deleted."
    except Exception as e:
        log.error(f"Memory clear failed: {e}")
        return "Could not clear memory."


def memory_stats() -> str:
    try:
        count = _col.count()
        return f"Memory contains {count} stored interactions."
    except Exception:
        return "Memory unavailable."