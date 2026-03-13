import os
import subprocess
import pyautogui
import webbrowser
from langchain_core.tools import tool

WINDOWS_APP_PATHS = {
    "chrome":      r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "chrome_alt":  r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "whatsapp":    os.path.join(os.environ.get("LOCALAPPDATA", ""), "WhatsApp", "WhatsApp.exe"),
    "notepad":     "notepad.exe",
    "calculator":  "calc.exe",
    "explorer":    "explorer.exe",
    "vscode":      os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Microsoft VS Code", "Code.exe"),
    "spotify":     os.path.join(os.environ.get("APPDATA", ""), "Spotify", "Spotify.exe"),
    "word":        r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel":       r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
}

BROWSER_URLS = {
    "whatsapp":  "https://web.whatsapp.com",
    "youtube":   "https://www.youtube.com",
    "gmail":     "https://mail.google.com",
    "maps":      "https://maps.google.com",
    "instagram": "https://www.instagram.com",
    "twitter":   "https://www.twitter.com",
    "linkedin":  "https://www.linkedin.com",
    "github":    "https://www.github.com",
}

@tool
def open_application(app_name: str) -> str:
    """Open any application or website. Examples: chrome, whatsapp, youtube, notepad, calculator, spotify, vscode"""
    name = app_name.lower().strip()

    # Website urls
    if name in BROWSER_URLS:
        try:
            webbrowser.open(BROWSER_URLS[name])
            return f"Opened {app_name} in browser."
        except Exception as e:
            return f"Browser open failed: {e}"

    # Direct .exe paths
    if name in WINDOWS_APP_PATHS:
        path = WINDOWS_APP_PATHS[name]
        if os.path.exists(path):
            subprocess.Popen([path])
            return f"Opened {app_name}."

    # Chrome fallback paths
    if name == "chrome":
        for path in [WINDOWS_APP_PATHS["chrome"], WINDOWS_APP_PATHS["chrome_alt"]]:
            if os.path.exists(path):
                subprocess.Popen([path])
                return "Opened Chrome."
        webbrowser.open("https://www.google.com")
        return "Opened default browser."

    # Try Windows 'start' command
    try:
        subprocess.Popen(["start", app_name], shell=True)
        return f"Opened {app_name}."
    except Exception:
        pass

    # Try webbrowser as last resort
    try:
        webbrowser.open(f"https://www.{name}.com")
        return f"Opened {app_name} in browser."
    except Exception as e:
        return f"Could not open {app_name}: {e}"

@tool
def list_files(folder_path: str = ".") -> str:
    """List files in a folder. Defaults to current directory."""
    try:
        files = os.listdir(folder_path)
        return f"Files in {folder_path}:\n" + "\n".join(files)
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def take_screenshot(filename: str = "screenshot.png") -> str:
    """Take a screenshot and save it."""
    try:
        path = os.path.join(os.path.expanduser("~"), filename)
        pyautogui.screenshot(path)
        return f"Screenshot saved to {path}"
    except Exception as e:
        return f"Screenshot failed: {str(e)}"

@tool
def get_system_info(_: str = "") -> str:
    """Get basic system information like OS, CPU, memory."""
    import platform
    info = {
        "OS":      platform.system(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Python":  platform.python_version(),
    }
    return "\n".join([f"{k}: {v}" for k, v in info.items()])