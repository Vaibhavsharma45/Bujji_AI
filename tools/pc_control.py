import os
import subprocess
import pyautogui
from langchain.tools import tool

@tool
def open_application(app_name: str) -> str:
    """Open any application on the computer by name. Example: chrome, notepad, calculator."""
    app_map = {
        "chrome":     "google-chrome",
        "firefox":    "firefox",
        "notepad":    "notepad" if os.name == "nt" else "gedit",
        "calculator": "calc"    if os.name == "nt" else "gnome-calculator",
        "terminal":   "cmd"     if os.name == "nt" else "gnome-terminal",
        "files":      "explorer" if os.name == "nt" else "nautilus",
    }
    cmd = app_map.get(app_name.lower(), app_name)
    try:
        if os.name == "nt":
            os.startfile(cmd)
        else:
            subprocess.Popen([cmd])
        return f"Opened {app_name} successfully."
    except Exception as e:
        return f"Could not open {app_name}: {str(e)}"

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