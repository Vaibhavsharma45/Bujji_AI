"""
api/server.py — FastAPI REST API for BUJJI
Run: uvicorn api.server:app --reload
Endpoints: /ask, /memory/stats, /memory/clear, /health
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

from brain  import ask_jarvis, clear_history
from memory import memory_stats, clear_memory
from config import VERSION, BUJJI_NAME
from logger import get_logger

log = get_logger("api")

app = FastAPI(
    title=f"{BUJJI_NAME} API",
    description="REST API for BUJJI Personal AI Assistant",
    version=VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    query: str
    emotion: str = "neutral"

class AskResponse(BaseModel):
    response: str
    emotion:  str
    timestamp: str


@app.get("/health")
def health():
    return {"status": "online", "assistant": BUJJI_NAME, "version": VERSION,
            "timestamp": datetime.now().isoformat()}

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    log.info(f"API /ask → {req.query[:80]}")
    try:
        resp = ask_jarvis(req.query, req.emotion)
        return AskResponse(response=resp, emotion=req.emotion,
                           timestamp=datetime.now().isoformat())
    except Exception as e:
        log.error(f"API error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memory/stats")
def mem_stats():
    return {"stats": memory_stats()}

@app.delete("/memory")
def mem_clear():
    return {"result": clear_memory()}

@app.delete("/history")
def hist_clear():
    return {"result": clear_history()}