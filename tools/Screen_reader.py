import subprocess, sys, os, base64, tempfile
from langchain_core.tools import tool
from logger import get_logger

log = get_logger("tool.screen")

@tool
def read_screen() -> str:
    """Take a screenshot and read all text visible on screen using OCR."""
    try:
        import pyautogui
        from PIL import Image
        import pytesseract

        # Screenshot
        img = pyautogui.screenshot()
        text = pytesseract.image_to_string(img)
        text = text.strip()
        if not text:
            return "Screen pe koi readable text nahi mila."
        # Return first 800 chars (enough for context)
        return "Screen pe yeh text dikh raha hai:\n" + text[:800]
    except ImportError as e:
        return f"Missing library: {e}. Run: pip install pytesseract pillow pyautogui"
    except Exception as e:
        log.error(f"Screen read error: {e}")
        return f"Screen read failed: {e}"

@tool
def read_selected_text() -> str:
    """Read the currently selected/highlighted text on screen."""
    try:
        import pyperclip
        import pyautogui
        import time

        # Copy selected text to clipboard
        pyautogui.hotkey("ctrl", "c")
        time.sleep(0.3)
        text = pyperclip.paste().strip()
        if not text:
            return "Koi text selected nahi hai. Pehle kuch select karo."
        return f"Selected text: {text[:600]}"
    except Exception as e:
        return f"Error: {e}"

@tool
def search_on_screen(query: str) -> str:
    """Search for specific text on the current screen using OCR."""
    try:
        import pyautogui
        import pytesseract

        img = pyautogui.screenshot()
        text = pytesseract.image_to_string(img).lower()
        if query.lower() in text:
            return f"Haan, '{query}' screen pe dikh raha hai."
        return f"Nahi, '{query}' screen pe visible nahi hai abhi."
    except ImportError:
        return "pip install pytesseract pillow pyautogui"
    except Exception as e:
        return f"Error: {e}"