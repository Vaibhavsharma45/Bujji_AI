import os, subprocess
from langchain_core.tools import tool
from logger import get_logger
log = get_logger("tool.self")

@tool
def type_text(text: str) -> str:
    """Type any text at current cursor position."""
    try:
        import pyautogui
        pyautogui.write(text, interval=0.03)
        return "Typed: " + text[:50]
    except Exception as e:
        return "Type error: " + str(e)

@tool
def press_key(key: str) -> str:
    """Press keyboard key or shortcut e.g. enter, escape, ctrl+c, alt+tab."""
    try:
        import pyautogui
        keys = [k.strip() for k in key.lower().split("+")]
        if len(keys) == 1:
            pyautogui.press(keys[0])
        else:
            pyautogui.hotkey(*keys)
        return "Pressed: " + key
    except Exception as e:
        return "Key error: " + str(e)

@tool
def click_screen(x: int, y: int) -> str:
    """Click at screen coordinates (x, y)."""
    try:
        import pyautogui
        pyautogui.click(x, y)
        return "Clicked at (" + str(x) + ", " + str(y) + ")."
    except Exception as e:
        return "Click error: " + str(e)

@tool
def scroll_screen(direction: str = "down", amount: int = 3) -> str:
    """Scroll screen up or down."""
    try:
        import pyautogui
        pyautogui.scroll(amount if direction == "up" else -amount)
        return "Scrolled " + direction
    except Exception as e:
        return "Scroll error: " + str(e)

@tool
def get_clipboard_content() -> str:
    """Read current clipboard content."""
    try:
        import pyperclip
        c = pyperclip.paste()
        return "Clipboard: " + c[:400] if c else "Clipboard empty."
    except Exception as e:
        return "Clipboard error: " + str(e)

@tool
def run_terminal_command(command: str) -> str:
    """Run a safe terminal command and return output. E.g. ipconfig, dir, tasklist."""
    blocked = ["rm ", "del ", "format ", "shutdown ", "rmdir /s", "mkfs", ":(){"]
    if any(b in command.lower() for b in blocked):
        return "Blocked for safety."
    try:
        r = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=15)
        out = r.stdout.strip() or r.stderr.strip()
        return out[:600] if out else "No output."
    except subprocess.TimeoutExpired:
        return "Timed out."
    except Exception as e:
        return "Error: " + str(e)

@tool
def lock_screen() -> str:
    """Lock the Windows screen immediately."""
    try:
        import ctypes
        ctypes.windll.user32.LockWorkStation()
        return "Screen locked bhaiya."
    except Exception as e:
        return "Lock error: " + str(e)

@tool
def set_volume(level: int) -> str:
    """Set Windows system volume from 0 to 100."""
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        level = max(0, min(100, level))
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(level / 100.0, None)
        return "Volume " + str(level) + "% set bhaiya."
    except ImportError:
        return "pip install pycaw comtypes"
    except Exception as e:
        return "Volume error: " + str(e)

@tool
def mute_unmute() -> str:
    """Toggle system mute on or off."""
    try:
        import pyautogui
        pyautogui.press("volumemute")
        return "Mute toggled bhaiya."
    except Exception as e:
        return "Mute error: " + str(e)

@tool
def open_file(filepath: str) -> str:
    """Open any file with its default application."""
    try:
        import platform
        if not os.path.exists(filepath):
            return "File not found: " + filepath
        if platform.system() == "Windows":
            os.startfile(filepath)
        return "Opened: " + filepath
    except Exception as e:
        return "Error: " + str(e)
