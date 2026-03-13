import os, subprocess, time
from langchain_core.tools import tool
from logger import get_logger

log = get_logger("tool.self")

@tool
def type_text(text: str) -> str:
    """Type any text at the current cursor position using keyboard automation."""
    try:
        import pyautogui
        pyautogui.write(text, interval=0.03)
        return f"Typed: {text[:50]}"
    except ImportError:
        return "pip install pyautogui"
    except Exception as e:
        return f"Type error: {e}"

@tool
def press_key(key: str) -> str:
    """Press a keyboard key or shortcut. Examples: enter, escape, ctrl+c, alt+tab, win."""
    try:
        import pyautogui
        keys = [k.strip() for k in key.lower().split("+")]
        if len(keys) == 1:
            pyautogui.press(keys[0])
        else:
            pyautogui.hotkey(*keys)
        return f"Pressed: {key}"
    except ImportError:
        return "pip install pyautogui"
    except Exception as e:
        return f"Key error: {e}"

@tool
def click_screen(x: int, y: int) -> str:
    """Click at specific screen coordinates (x, y pixels from top-left)."""
    try:
        import pyautogui
        pyautogui.click(x, y)
        return f"Clicked at ({x}, {y})."
    except ImportError:
        return "pip install pyautogui"
    except Exception as e:
        return f"Click error: {e}"

@tool
def scroll_screen(direction: str = "down", amount: int = 3) -> str:
    """Scroll the screen. direction: up or down. amount: scroll steps."""
    try:
        import pyautogui
        clicks = amount if direction == "up" else -amount
        pyautogui.scroll(clicks)
        return f"Scrolled {direction} by {amount}."
    except Exception as e:
        return f"Scroll error: {e}"

@tool
def get_clipboard_content() -> str:
    """Read current clipboard content."""
    try:
        import pyperclip
        content = pyperclip.paste()
        return f"Clipboard: {content[:400]}" if content else "Clipboard is empty."
    except Exception as e:
        return f"Clipboard error: {e}"

@tool
def run_terminal_command(command: str) -> str:
    """
    Run a terminal/cmd command and return output.
    Safe commands only: dir, ipconfig, ping, tasklist, echo, python --version, etc.
    """
    BLOCKED = ["rm", "del", "format", "shutdown", "mkfs", "dd ", ":(){", "rmdir /s"]
    if any(b in command.lower() for b in BLOCKED):
        return "That command is blocked for safety reasons."
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=15
        )
        output = result.stdout.strip() or result.stderr.strip()
        return output[:600] if output else "Command ran with no output."
    except subprocess.TimeoutExpired:
        return "Command timed out (15s limit)."
    except Exception as e:
        return f"Command error: {e}"

@tool
def lock_screen() -> str:
    """Lock the Windows screen."""
    try:
        import ctypes
        ctypes.windll.user32.LockWorkStation()
        return "Screen locked."
    except Exception as e:
        return f"Lock error: {e}"

@tool
def set_volume(level: int) -> str:
    """Set Windows system volume. level: 0 to 100."""
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        level = max(0, min(100, level))
        volume.SetMasterVolumeLevelScalar(level / 100.0, None)
        return f"System volume set to {level}%."
    except ImportError:
        return "pip install pycaw comtypes"
    except Exception as e:
        return f"Volume error: {e}"

@tool
def mute_unmute() -> str:
    """Toggle system mute/unmute."""
    try:
        import pyautogui
        pyautogui.press("volumemute")
        return "Mute toggled."
    except Exception as e:
        return f"Mute error: {e}"

@tool
def open_file(filepath: str) -> str:
    """Open any file with its default application."""
    try:
        import os, platform
        if not os.path.exists(filepath):
            return f"File not found: {filepath}"
        if platform.system() == "Windows":
            os.startfile(filepath)
        else:
            subprocess.Popen(["xdg-open", filepath])
        return f"Opened: {filepath}"
    except Exception as e:
        return f"Open error: {e}"