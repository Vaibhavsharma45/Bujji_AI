"""
tools/monitor.py — Background System Monitor
Polls CPU, RAM, battery at intervals and fires voice alerts when thresholds exceeded.
"""
import threading
import time
from langchain_core.tools import tool
from config import MONITOR_CPU_THRESHOLD, MONITOR_RAM_THRESHOLD, MONITOR_BATTERY_LOW, MONITOR_INTERVAL
from logger import get_logger

log = get_logger("tool.monitor")

_thread:     threading.Thread | None = None
_monitoring: bool  = False
_config:     dict  = {}


def _alert(msg: str):
    from voice import speak
    log.warning(f"ALERT: {msg}")
    speak(msg)


def _loop():
    global _monitoring
    try:
        import psutil
    except ImportError:
        log.error("psutil not installed")
        return

    log.info(f"Monitor running — CPU>{_config['cpu']}% RAM>{_config['ram']}% every {_config['interval']}s")

    while _monitoring:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent

        if cpu > _config["cpu"]:
            _alert(f"Warning sir — CPU at {cpu:.0f} percent, something is heavy!")
        if ram > _config["ram"]:
            _alert(f"Warning sir — RAM at {ram:.0f} percent, consider closing apps.")

        batt = getattr(psutil, "sensors_battery", lambda: None)()
        if batt and not batt.power_plugged and batt.percent < _config["batt_low"]:
            _alert(f"Low battery alert — {batt.percent:.0f} percent remaining. Please plug in.")

        time.sleep(_config["interval"] - 1)  # -1 to account for cpu_percent(interval=1)


@tool
def start_system_monitor(cpu_threshold: int = MONITOR_CPU_THRESHOLD,
                         ram_threshold: int = MONITOR_RAM_THRESHOLD,
                         interval_seconds: int = MONITOR_INTERVAL) -> str:
    """
    Start a background monitor that alerts when CPU/RAM exceed thresholds.
    cpu_threshold: alert when CPU% exceeds this (default 85).
    ram_threshold: alert when RAM% exceeds this (default 85).
    interval_seconds: check interval (default 30).
    """
    global _thread, _monitoring, _config
    if _monitoring:
        return "Monitor already running."
    _config = {
        "cpu": cpu_threshold, "ram": ram_threshold,
        "batt_low": MONITOR_BATTERY_LOW, "interval": interval_seconds
    }
    _monitoring = True
    _thread     = threading.Thread(target=_loop, daemon=True)
    _thread.start()
    return f"System monitor started — alerting when CPU>{cpu_threshold}% or RAM>{ram_threshold}%."


@tool
def stop_system_monitor() -> str:
    """Stop the background system monitor."""
    global _monitoring
    _monitoring = False
    return "System monitor stopped."