import time, threading
from langchain_core.tools import tool
from logger import get_logger

log = get_logger("tool.whatsapp_reader")

_last_messages = []

@tool
def read_whatsapp_messages(contact_name: str = "") -> str:
    """
    Read recent WhatsApp messages from WhatsApp Web using browser automation.
    contact_name: specific contact to read from (optional, reads recent if empty).
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        opts = Options()
        opts.add_argument("--user-data-dir=./whatsapp_session")  # saves login
        opts.add_argument("--profile-directory=Default")
        opts.add_experimental_option("excludeSwitches", ["enable-logging"])

        driver = webdriver.Chrome(options=opts)
        driver.get("https://web.whatsapp.com")

        # Wait for WhatsApp to load (scan QR first time)
        wait = WebDriverWait(driver, 60)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="chat-list"]' )))

        messages = []

        if contact_name:
            # Search for specific contact
            search = driver.find_element(By.CSS_SELECTOR, '[data-testid="chat-list-search"]')
            search.clear()
            search.send_keys(contact_name)
            time.sleep(2)

            chats = driver.find_elements(By.CSS_SELECTOR, '[data-testid="cell-frame-container"]')
            if chats:
                chats[0].click()
                time.sleep(2)

                # Read last 5 messages
                msgs = driver.find_elements(By.CSS_SELECTOR, '.message-in .copyable-text, .message-out .copyable-text')
                for m in msgs[-5:]:
                    try:
                        messages.append(m.get_attribute("data-pre-plain-text") + m.text)
                    except Exception:
                        messages.append(m.text)
        else:
            # Read recent unread counts from chat list
            chats = driver.find_elements(By.CSS_SELECTOR, '[data-testid="cell-frame-container"]')[:5]
            for chat in chats:
                try:
                    name = chat.find_element(By.CSS_SELECTOR, '[data-testid="cell-frame-title"]').text
                    try:
                        badge = chat.find_element(By.CSS_SELECTOR, '[data-testid="icon-unread-count"]').text
                        messages.append(f"{name}: {badge} unread messages")
                    except Exception:
                        messages.append(f"{name}: no unread")
                except Exception:
                    pass

        driver.quit()
        if not messages:
            return "Koi messages nahi mile."
        return "WhatsApp messages:\n" + "\n".join(messages)

    except ImportError:
        return "pip install selenium  aur  chromedriver install karo"
    except Exception as e:
        log.error(f"WhatsApp reader error: {e}")
        return f"WhatsApp reader error: {e}"


@tool
def get_whatsapp_unread_count() -> str:
    """Get count of unread WhatsApp messages from WhatsApp Web."""
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        opts = Options()
        opts.add_argument("--user-data-dir=./whatsapp_session")
        opts.add_argument("--profile-directory=Default")
        opts.add_experimental_option("excludeSwitches", ["enable-logging"])

        driver = webdriver.Chrome(options=opts)
        driver.get("https://web.whatsapp.com")
        wait = WebDriverWait(driver, 60)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="chat-list"]' )))

        badges = driver.find_elements(By.CSS_SELECTOR, '[data-testid="icon-unread-count"]')
        total = sum(int(b.text) for b in badges if b.text.isdigit())
        driver.quit()
        return f"Total {total} unread WhatsApp messages hain."
    except ImportError:
        return "pip install selenium"
    except Exception as e:
        return f"Error: {e}"