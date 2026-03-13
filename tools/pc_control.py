"""
tools/pc_control.py — PC Automation Tools
Open apps/websites, manage files, take screenshots, control clipboard.
"""
import os
import webbrowser
import subprocess
import platform
import shutil
from datetime import datetime
from langchain_core.tools import tool
from logger import get_logger

log = get_logger("tool.pc")

# ── URL registry ───────────────────────────────────────────────────────────────
BROWSER_URLS: dict[str, str] = {
    "youtube":       "https://youtube.com",
    "gmail":         "https://mail.google.com",
    "email":         "https://mail.google.com",
    "whatsapp":      "https://web.whatsapp.com",
    "chatgpt":       "https://chat.openai.com",
    "openai":        "https://openai.com",
    "github":        "https://github.com",
    "kaggle":        "https://kaggle.com",
    "colab":         "https://colab.research.google.com",
    "instagram":     "https://instagram.com",
    "twitter":       "https://twitter.com",
    "x":             "https://twitter.com",
    "linkedin":      "https://linkedin.com",
    "netflix":       "https://netflix.com",
    "google":        "https://google.com",
    "maps":          "https://maps.google.com",
    "amazon":        "https://amazon.in",
    "flipkart":      "https://flipkart.com",
    "dailymotion":   "https://dailymotion.com",
    "spotify":       "https://open.spotify.com",
    "reddit":        "https://reddit.com",
    "stackoverflow": "https://stackoverflow.com",
    "discord":       "https://discord.com/app",
    "notion":        "https://notion.so",
    "huggingface":   "https://huggingface.co",
    "leetcode":      "https://leetcode.com",
}

# ── Windows app registry ───────────────────────────────────────────────────────
WIN_APPS: dict[str, str] = {
    "chrome":       "chrome",
    "firefox":      "firefox",
    "notepad":      "notepad",
    "calculator":   "calc",
    "paint":        "mspaint",
    "excel":        "excel",
    "word":         "winword",
    "powerpoint":   "powerpnt",
    "vscode":       "code",
    "terminal":     "wt",
    "cmd":          "cmd",
    "explorer":     "explorer",
    "task manager": "taskmgr",
    "snipping tool":"snippingtool",
    "settings":     "ms-settings:",
}


@tool
def open_application(app_name: str) -> str:
    """
    Open any app or website by name. Call ONCE — do not retry.
    Supported app names: chrome, firefox, notepad, calculator, paint, excel, word,
    powerpoint, vscode, terminal, cmd, explorer, settings,
    youtube, gmail, email, whatsapp, chatgpt, github, kaggle, colab,
    instagram, twitter, linkedin, netflix, google, maps, amazon, flipkart,
    spotify, reddit, stackoverflow, discord, notion, huggingface, leetcode.
    """
    name = app_name.lower().strip().replace(" ", "")
    log.info(f"Opening: {name}")

    # 1. Browser URL
    if name in BROWSER_URLS:
        webbrowser.open(BROWSER_URLS[name])
        return f"Opened {name}."

    # 2. Windows native app
    if platform.system() == "Windows":
        cmd = WIN_APPS.get(name, name)
        try:
            subprocess.Popen(cmd, shell=True,
                             creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
            return f"Launched {name}."
        except Exception as e:
            log.error(f"Win launch error: {e}")

    # 3. macOS
    if platform.system() == "Darwin":
        try:
            subprocess.Popen(["open", "-a", name])
            return f"Opened {name}."
        except Exception as e:
            pass

    # 4. Generic URL fallback
    try:
        webbrowser.open(f"https://{name}.com")
        return f"Tried opening {name}.com in browser."
    except Exception as e:
        return f"Could not open {name}: {e}"


@tool
def list_files(directory: str = "~") -> str:
    """List files and folders in a directory. Defaults to home directory."""
    try:
        path  = os.path.expanduser(directory)
        items = os.listdir(path)
        dirs  = sorted([i for i in items if os.path.isdir(os.path.join(path, i))])[:10]
        files = sorted([i for i in items if os.path.isfile(os.path.join(path, i))])[:20]
        size  = sum(os.path.getsize(os.path.join(path, f)) for f in files if os.path.isfile(os.path.join(path, f)))
        return (
            f"Directory: {path}\n"
            f"Folders ({len(dirs)}): {', '.join(dirs) or 'none'}\n"
            f"Files ({len(files)}): {', '.join(files) or 'none'}\n"
            f"Total size: {size // 1024} KB"
        )
    except Exception as e:
        return f"Error listing {directory}: {e}"


@tool
def take_screenshot(filename: str = "") -> str:
    """Take a screenshot and save it to the Desktop."""
    try:
        import pyautogui
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        os.makedirs(desktop, exist_ok=True)
        fname = filename or f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        if not fname.endswith(".png"):
            fname += ".png"
        path  = os.path.join(desktop, fname)
        pyautogui.screenshot(path)
        return f"Screenshot saved to Desktop: {fname}"
    except ImportError:
        return "Install pyautogui: pip install pyautogui"
    except Exception as e:
        return f"Screenshot failed: {e}"


@tool
def get_system_info() -> str:
    """Get CPU, RAM, disk, battery, and uptime info."""
    try:
        import psutil
        cpu   = psutil.cpu_percent(interval=1)
        ram   = psutil.virtual_memory()
        disk  = psutil.disk_usage("/")
        boot  = datetime.fromtimestamp(psutil.boot_time())
        upt   = datetime.now() - boot
        uph   = upt.seconds // 3600
        upm   = (upt.seconds % 3600) // 60

        batt_str = ""
        if hasattr(psutil, "sensors_battery"):
            b = psutil.sensors_battery()
            if b:
                status = "charging" if b.power_plugged else "on battery"
                batt_str = f"\nBattery: {b.percent:.0f}% ({status})"

        return (
            f"CPU: {cpu:.1f}% | Cores: {psutil.cpu_count(logical=False)} physical, {psutil.cpu_count()} logical\n"
            f"RAM: {ram.percent:.1f}% used — {ram.used/1024**3:.1f} GB / {ram.total/1024**3:.1f} GB\n"
            f"Disk: {disk.percent:.1f}% used — {disk.used/1024**3:.0f} GB / {disk.total/1024**3:.0f} GB\n"
            f"Uptime: {uph}h {upm}m{batt_str}"
        )
    except ImportError:
        return "Install psutil: pip install psutil"
    except Exception as e:
        return f"System info error: {e}"


@tool
def copy_to_clipboard(text: str) -> str:
    """Copy text to the system clipboard."""
    try:
        import pyperclip
        pyperclip.copy(text)
        preview = text[:60] + ("..." if len(text) > 60 else "")
        return f"Copied to clipboard: {preview}"
    except ImportError:
        return "Install pyperclip: pip install pyperclip"
    except Exception as e:
        return f"Clipboard error: {e}"


@tool
def kill_process(process_name: str) -> str:
    """Kill a running process by name. E.g. 'chrome', 'notepad'."""
    try:
        import psutil
        killed = []
        for proc in psutil.process_iter(["name", "pid"]):
            if process_name.lower() in proc.info["name"].lower():
                proc.kill()
                killed.append(proc.info["name"])
        return f"Killed: {', '.join(killed)}" if killed else f"No process named {process_name} found."
    except ImportError:
        return "Install psutil: pip install psutil"
    except Exception as e:
        return f"Kill process error: {e}"


@tool
def get_top_processes() -> str:
    """List top 5 CPU-consuming processes running right now."""
    try:
        import psutil
        procs = sorted(
            psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]),
            key=lambda p: p.info["cpu_percent"] or 0,
            reverse=True,
        )[:5]
        lines = [
            f"{p.info['name'][:22]:<24} CPU:{p.info['cpu_percent']:5.1f}%  RAM:{p.info['memory_percent']:4.1f}%"
            for p in procs
        ]
        return "Top processes:\n" + "\n".join(lines)
    except ImportError:
        return "Install psutil: pip install psutil"
    except Exception as e:
        return f"Process list error: {e}"