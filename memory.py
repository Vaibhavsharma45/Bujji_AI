import chromadb
from datetime import datetime

client     = chromadb.Client()
collection = client.get_or_create_collection("jarvis_memory")

def save_memory(user_input: str, jarvis_response: str):
    doc_id = f"mem_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    collection.add(
        documents=[f"User: {user_input}\nJARVIS: {jarvis_response}"],
        ids=[doc_id],
        metadatas=[{"timestamp": datetime.now().isoformat()}]
    )

def get_relevant_memory(query: str, n: int = 3) -> str:
    try:
        results = collection.query(query_texts=[query], n_results=n)
        docs = results.get("documents", [[]])[0]
        if not docs:
            return ""
        return "\n---\n".join(docs)
    except Exception:
        return ""

def clear_memory():
    ids = collection.get()["ids"]
    if ids:
        collection.delete(ids=ids)
    return "Memory cleared."