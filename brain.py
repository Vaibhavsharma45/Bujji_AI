from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from config import GROQ_API_KEY, GROQ_MODEL, AGENT_RECURSION_LIMIT, CHAT_HISTORY_MAX
from memory import get_relevant_memory, save_memory
from logger import get_logger
from tools.search import web_search, search_news
from tools.pc_control import open_application, list_files, take_screenshot, get_system_info, copy_to_clipboard, kill_process, get_top_processes
from tools.email_tool import send_email
from tools.whatsapp import send_whatsapp
from tools.monitor import start_system_monitor, stop_system_monitor
from tools.reminder import set_reminder, list_reminders, clear_reminders
from tools.calculator import calculate, convert_units, get_datetime_info

log = get_logger("brain")

ALL_TOOLS = [
    web_search, search_news,
    open_application, list_files, take_screenshot,
    get_system_info, copy_to_clipboard, kill_process, get_top_processes,
    send_email, send_whatsapp,
    start_system_monitor, stop_system_monitor,
    set_reminder, list_reminders, clear_reminders,
    calculate, convert_units, get_datetime_info,
]

def _try_import(module, names):
    try:
        import importlib
        mod = importlib.import_module(module)
        loaded = [getattr(mod, n) for n in names]
        ALL_TOOLS.extend(loaded)
        log.info("Loaded: " + module + " (" + str(len(loaded)) + " tools)")
    except Exception as e:
        log.debug("Skipped " + module + ": " + str(e))

_try_import("tools.screen_reader",    ["read_screen", "read_selected_text", "search_on_screen"])
_try_import("tools.spotify_control",  ["spotify_play", "spotify_pause", "spotify_next", "spotify_previous", "spotify_volume", "spotify_current_song"])
_try_import("tools.whatsapp_reader",  ["read_whatsapp_messages", "get_whatsapp_unread_count"])
_try_import("tools.self_assistance",  ["type_text", "press_key", "click_screen", "scroll_screen", "get_clipboard_content", "run_terminal_command", "lock_screen", "set_volume", "mute_unmute", "open_file"])
_try_import("tools.autonomous_agent", ["autonomous_web_research", "autonomous_youtube_play", "autonomous_scrape_website", "autonomous_browser_task", "autonomous_fill_form"])

log.info("Total tools loaded: " + str(len(ALL_TOOLS)))

_llm = ChatGroq(api_key=GROQ_API_KEY, model_name=GROQ_MODEL, temperature=0, max_tokens=256)

FRIDAY_SYSTEM = (
    "You are FRIDAY, Vaibhav bhaiya ka personal AI assistant. "
    "Casual, friendly, Hinglish. Max 1-2 lines. Confident. "
    "CRITICAL: Never say 'Final Answer:' or 'The final answer is'. Just reply directly. "
    "TOOL RULES: Call each tool EXACTLY ONCE. After tool returns result -> reply directly. Stop. "
    "open_application app_name must be one lowercase word only: "
    "chrome firefox notepad calculator paint excel word powerpoint vscode "
    "terminal cmd explorer youtube gmail email whatsapp chatgpt github "
    "kaggle colab instagram twitter linkedin netflix google maps amazon "
    "flipkart spotify reddit stackoverflow discord notion. "
    "volume badhao/kam karo/set karo -> set_volume tool (0-100). "
    "mute -> mute_unmute tool. "
    "youtube pe song play -> autonomous_youtube_play tool. "
    "web research -> autonomous_web_research tool. "
    "screen padho -> read_screen tool. "
    "lock karo -> lock_screen tool. "
    "type karo -> type_text tool."
)

_agent = create_react_agent(_llm, ALL_TOOLS)
_chat_history = []

def _clean_response(text):
    import re
    text = re.sub(r"(?i)final answer[:\s]*", "", text)
    text = re.sub(r"(?i)the final answer is[:\s]*", "", text)
    text = re.sub(r"(?i)action input[:\s]*", "", text)
    text = text.strip().strip(".")
    return text if text else "Ho gaya bhaiya!"

def ask_jarvis(user_input, emotion="neutral"):
    global _chat_history
    from tools.emotion import emotion_tone_hint
    tone = emotion_tone_hint(emotion)
    mem_ctx = get_relevant_memory(user_input)
    system = FRIDAY_SYSTEM
    if tone:
        system = system + " TONE: " + tone
    if mem_ctx:
        system = system + " CONTEXT: " + mem_ctx
    messages = ([SystemMessage(content=system)]
                + _chat_history[-CHAT_HISTORY_MAX:]
                + [HumanMessage(content=user_input)])
    log.info("Query: " + user_input[:80])
    try:
        result = _agent.invoke(
            {"messages": messages},
            config={"recursion_limit": AGENT_RECURSION_LIMIT},
        )
        answer = ""
        for msg in reversed(result["messages"]):
            if getattr(msg, "type", "") == "ai" and msg.content and msg.content.strip():
                answer = _clean_response(msg.content.strip())
                break
        if not answer:
            answer = "Ho gaya bhaiya!"
        _chat_history.append(HumanMessage(content=user_input))
        _chat_history.append(AIMessage(content=answer))
        if len(_chat_history) > CHAT_HISTORY_MAX:
            _chat_history = _chat_history[-CHAT_HISTORY_MAX:]
        save_memory(user_input, answer, emotion)
        log.info("Response: " + answer[:80])
        return answer
    except Exception as e:
        err = str(e)
        log.error("Agent error: " + err)
        if "recursion" in err.lower():
            return "Ho gaya bhaiya!"
        if "429" in err or "rate_limit" in err.lower():
            return "Bhaiya Groq rate limit, thoda wait karo!"
        if any(k in err for k in ["tool_use_failed", "400", "tool call validation"]):
            return "Dobara bolo bhaiya - jaise 'volume 70 karo' ya 'play Arijit Singh'."
        return "Kuch gadbad bhaiya: " + err[:80]

def clear_history():
    global _chat_history
    _chat_history = []
    return "Chat history clear bhaiya!"
