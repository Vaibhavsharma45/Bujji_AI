import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime

from brain  import ask_jarvis, clear_history
from memory import memory_stats, clear_memory, _col
from config import VERSION
from logger import get_logger

log = get_logger("api")

app = FastAPI(title="BUJJI FRIDAY API", version=VERSION)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class AskRequest(BaseModel):
    query: str
    emotion: str = "neutral"


@app.get("/")
def dashboard():
    path = os.path.join(os.path.dirname(__file__), "..", "ui", "dashboard.html")
    if os.path.exists(path):
        return FileResponse(path)
    return {"status": "BUJJI FRIDAY API online", "dashboard": "ui/dashboard.html not found"}


@app.post("/ask")
def ask(req: AskRequest):
    if not req.query.strip():
        raise HTTPException(400, "Query empty")
    log.info(f"/ask: {req.query[:80]}")
    try:
        resp = ask_jarvis(req.query, req.emotion)
        return {"response": resp, "emotion": req.emotion, "timestamp": datetime.now().isoformat()}
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/stats")
def get_stats():
    try:
        import psutil
        from datetime import datetime
        cpu  = psutil.cpu_percent(interval=0.5)
        ram  = psutil.virtual_memory().percent
        boot = datetime.fromtimestamp(psutil.boot_time())
        upt  = datetime.now() - boot
        uph  = upt.seconds // 3600
        upm  = (upt.seconds % 3600) // 60
        battery = "--"
        if hasattr(psutil, "sensors_battery"):
            b = psutil.sensors_battery()
            if b:
                battery = round(b.percent)
        try:
            mems = _col.count()
        except Exception:
            mems = "--"
        return {
            "cpu": round(cpu, 1),
            "ram": round(ram, 1),
            "battery": battery,
            "memories": mems,
            "uptime": f"{uph}h {upm}m",
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/health")
def health():
    return {"status": "online", "version": VERSION}

@app.get("/memory/stats")
def mem_stats():
    return {"stats": memory_stats()}

@app.delete("/memory")
def mem_clear():
    return {"result": clear_memory()}

@app.delete("/history")
def hist_clear():
    return {"result": clear_history()}