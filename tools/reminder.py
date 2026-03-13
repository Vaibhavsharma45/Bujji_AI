"""
tools/reminder.py — Smart Reminder System
Uses the `schedule` library. Runs in a single background thread.
Supports one-time, daily, and hourly reminders with voice alerts.
"""
import threading
import time
import schedule as _schedule
from langchain_core.tools import tool
from logger import get_logger

log = get_logger("tool.reminder")

_reminders:  dict  = {}   # uid → {time, msg, repeat}
_sched_live: bool  = False
_counter:    int   = 0


def _ensure_scheduler():
    global _sched_live
    if not _sched_live:
        _sched_live = True
        t = threading.Thread(target=_sched_loop, daemon=True)
        t.start()
        log.info("Scheduler thread started")


def _sched_loop():
    while True:
        _schedule.run_pending()
        time.sleep(1)


def _fire(uid: str, message: str, repeat: str):
    from voice import speak
    speak(f"Reminder sir — {message}")
    log.info(f"Reminder fired: {message}")
    if repeat == "once":
        _reminders.pop(uid, None)


@tool
def set_reminder(message: str, time_str: str, repeat: str = "once") -> str:
    """
    Set a voice reminder.
    message: what to remind about.
    time_str: 24h format HH:MM, e.g. '14:30' or '09:00'.
    repeat: 'once', 'daily', or 'hourly'.
    """
    global _counter
    _ensure_scheduler()
    _counter += 1
    uid = f"rem_{_counter}"

    def job():
        _fire(uid, message, repeat)

    try:
        if repeat == "hourly":
            _schedule.every().hour.do(job).tag(uid)
        else:
            _schedule.every().day.at(time_str).do(job).tag(uid)
    except Exception as e:
        return f"Invalid time format. Use HH:MM (e.g. 14:30). Error: {e}"

    _reminders[uid] = {"time": time_str, "message": message, "repeat": repeat}
    log.info(f"Reminder set: {uid} | {time_str} | {repeat} | {message}")
    return f"Reminder set — '{message}' at {time_str} ({repeat})."


@tool
def list_reminders() -> str:
    """List all active reminders."""
    if not _reminders:
        return "No active reminders."
    lines = [f"• [{v['time']}] {v['message']} ({v['repeat']})" for v in _reminders.values()]
    return "Active reminders:\n" + "\n".join(lines)


@tool
def clear_reminders() -> str:
    """Cancel and delete all active reminders."""
    _schedule.clear()
    _reminders.clear()
    return "All reminders cleared."