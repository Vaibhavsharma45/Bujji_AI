from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.prebuilt import create_react_agent

from config import GROQ_API_KEY, GROQ_MODEL, AGENT_RECURSION_LIMIT, CHAT_HISTORY_MAX
from memory import get_relevant_memory, save_memory
from logger import get_logger

from tools.search        import web_search, search_news
from tools.pc_control    import (open_application, list_files, take_screenshot,
                                  get_system_info, copy_to_clipboard,
                                  kill_process, get_top_processes)
from tools.email_tool    import send_email
from tools.whatsapp      import send_whatsapp
from tools.monitor       import start_system_monitor, stop_system_monitor
from tools.reminder      import set_reminder, list_reminders, clear_reminders
from tools.calculator    import calculate, convert_units, get_datetime_info
from tools.screen_reader import read_screen, read_selected_text, search_on_screen
from tools.spotify_control import (spotify_play, spotify_pause, spotify_next,
                                    spotify_previous, spotify_volume, spotify_current_song)
from tools.whatsapp_reader import read_whatsapp_messages, get_whatsapp_unread_count
from tools.self_assistance import (type_text, press_key, click_screen, scroll_screen,
                                    get_clipboard_content, run_terminal_command,
                                    lock_screen, set_volume, mute_unmute, open_file)

log = get_logger("brain")

_llm = ChatGroq(api_key=GROQ_API_KEY, model_name=GROQ_MODEL, temperature=0.1, max_tokens=512)

ALL_TOOLS = [
    web_search, search_news,
    open_application, list_files, take_screenshot,
    get_system_info, copy_to_clipboard, kill_process, get_top_processes,
    send_email, send_whatsapp,
    start_system_monitor, stop_system_monitor,
    set_reminder, list_reminders, clear_reminders,
    calculate, convert_units, get_datetime_info,
    read_screen, read_selected_text, search_on_screen,
    spotify_play, spotify_pause, spotify_next, spotify_previous,
    spotify_volume, spotify_current_song,
    read_whatsapp_messages, get_whatsapp_unread_count,
    type_text, press_key, click_screen, scroll_screen,
    get_clipboard_content, run_terminal_command,
    lock_screen, set_volume, mute_unmute, open_file,
]

FRIDAY_SYSTEM = (
    "You are FRIDAY — Vaibhav bhaiya ka personal AI assistant. "
    "Personality: casual, friendly, thoda desi, aur sach mein helpful. "
    "JARVIS ki tarah formal mat bolo — Friday ki tarah baat karo. "
    "Hinglish mein baat karo jab user Hindi ya Hinglish mein bole. "
    "Short responses — 1-2 lines max. Confidence ke saath bolo. "
    "Jab kuch funny ho toh acknowledge karo. "
    "Examples of Friday style: "
    "User: time kya hai -> FRIDAY: Bhaiya, abhi 3:45 PM hai. "
    "User: open youtube -> FRIDAY: Lo khulja YouTube! "
    "User: system kya chal raha hai -> FRIDAY: Sab theek hai bhaiya, CPU 23% aur RAM 45% pe chal raha hai. "
    "STRICT TOOL RULES: "
    "Call each tool EXACTLY ONCE. After tool returns -> Final Answer immediately. "
    "open_application app_name: one lowercase word only: "
    "chrome firefox notepad calculator paint excel word powerpoint vscode "
    "terminal cmd explorer youtube gmail email whatsapp chatgpt github "
    "kaggle colab instagram twitter linkedin netflix google maps amazon "
    "flipkart spotify reddit stackoverflow discord notion. "
    "open whatsapp/see whatsapp -> open_application app_name=whatsapp. "
    "play song on spotify -> spotify_play tool use karo. "
    "screen pe kya hai / screen padho -> read_screen tool. "
    "volume set karo -> set_volume tool. "
    "lock karo -> lock_screen tool."
)

_agent = create_react_agent(_llm, ALL_TOOLS)
_chat_history = []


def ask_jarvis(user_input, emotion="neutral"):
    global _chat_history

    from tools.emotion import emotion_tone_hint
    tone    = emotion_tone_hint(emotion)
    mem_ctx = get_relevant_memory(user_input)

    system = FRIDAY_SYSTEM
    if tone:
        system = system + " TONE ADJUST: " + tone
    if mem_ctx:
        system = system + " CONTEXT: " + mem_ctx

    messages = (
        [SystemMessage(content=system)]
        + _chat_history[-CHAT_HISTORY_MAX:]
        + [HumanMessage(content=user_input)]
    )

    log.info("Query: " + user_input[:80])

    try:
        result = _agent.invoke(
            {"messages": messages},
            config={"recursion_limit": AGENT_RECURSION_LIMIT},
        )

        answer = ""
        for msg in reversed(result["messages"]):
            if getattr(msg, "type", "") == "ai" and msg.content and msg.content.strip():
                answer = msg.content.strip()
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
            return "Bhaiya, Groq ka rate limit aa gaya. Thoda wait karo ya nayi key daalo."
        if any(k in err for k in ["tool_use_failed", "400", "tool call validation"]):
            return "Bhaiya, clearly bolo — jaise open whatsapp ya play Arijit Singh song."
        return "Kuch gadbad hai bhaiya: " + err[:80]


def clear_history():
    global _chat_history
    _chat_history = []
    return "Chat history clear kar di bhaiya!"