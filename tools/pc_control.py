import os
import subprocess
import pyautogui
import webbrowser
from langchain_core.tools import tool

WINDOWS_APP_PATHS = {
    "chrome":     r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "chrome_alt": r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "whatsapp":   os.path.join(os.environ.get("LOCALAPPDATA", ""), "WhatsApp", "WhatsApp.exe"),
    "notepad":    "notepad.exe",
    "calculator": "calc.exe",
    "explorer":   "explorer.exe",
    "vscode":     os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Microsoft VS Code", "Code.exe"),
    "spotify":    os.path.join(os.environ.get("APPDATA", ""), "Spotify", "Spotify.exe"),
}

BROWSER_URLS = {
    "whatsapp":    "https://web.whatsapp.com",
    "youtube":     "https://www.youtube.com",
    "gmail":       "https://mail.google.com",
    "maps":        "https://maps.google.com",
    "instagram":   "https://www.instagram.com",
    "twitter":     "https://www.twitter.com",
    "linkedin":    "https://www.linkedin.com",
    "github":      "https://www.github.com",
    "openai":      "https://www.openai.com",
    "chatgpt":     "https://chat.openai.com",
    "claude":      "https://claude.ai",
    "gemini":      "https://gemini.google.com",
    "stackoverflow": "https://stackoverflow.com",
    "kaggle":      "https://www.kaggle.com",
    "colab":       "https://colab.research.google.com",
    "dailymotion": "https://www.dailymotion.com",
    "netflix":     "https://www.netflix.com",
    "amazon":      "https://www.amazon.in",
    "flipkart":    "https://www.flipkart.com",
    "google":      "https://www.google.com",
}

@tool
def open_application(app_name: str) -> str:
    """Open any application or website by name. Use exact names like: chrome, whatsapp, youtube, chatgpt, openai, gmail, github, spotify, notepad, calculator, vscode, kaggle, colab"""
    name = app_name.lower().strip().replace(" ", "")

    # Website check
    if name in BROWSER_URLS:
        webbrowser.open(BROWSER_URLS[name])
        return f"Opened {app_name}."

    # Exe path check
    if name in WINDOWS_APP_PATHS:
        path = WINDOWS_APP_PATHS[name]
        if os.path.exists(path):
            subprocess.Popen([path])
            return f"Opened {app_name}."

    # Chrome special
    if name == "chrome":
        for p in [WINDOWS_APP_PATHS["chrome"], WINDOWS_APP_PATHS["chrome_alt"]]:
            if os.path.exists(p):
                subprocess.Popen([p])
                return "Opened Chrome."
        webbrowser.open("https://www.google.com")
        return "Opened default browser."

    # Builtins
    if name in ["notepad", "calc", "mspaint", "explorer", "cmd", "taskmgr"]:
        subprocess.Popen([name])
        return f"Opened {name}."

    return f"'{app_name}' nahi pehchana. Yeh try karo: {', '.join(list(BROWSER_URLS.keys())[:10])}"

@tool
def list_files(folder_path: str = ".") -> str:
    """List files in a folder."""
    try:
        return f"Files in {folder_path}:\n" + "\n".join(os.listdir(folder_path))
    except Exception as e:
        return f"Error: {e}"

@tool
def take_screenshot(filename: str = "screenshot.png") -> str:
    """Take a screenshot and save it."""
    try:
        path = os.path.join(os.path.expanduser("~"), filename)
        pyautogui.screenshot(path)
        return f"Screenshot saved: {path}"
    except Exception as e:
        return f"Failed: {e}"

@tool
def get_system_info(_: str = "") -> str:
    """Get system information."""
    import platform
    return "\n".join([f"{k}: {v}" for k, v in {
        "OS": platform.system(), "Version": platform.version(),
        "Machine": platform.machine(), "Python": platform.python_version(),
    }.items()])