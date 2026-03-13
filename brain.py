from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.prebuilt import create_react_agent

from config import GROQ_API_KEY, GROQ_MODEL, AGENT_RECURSION_LIMIT, CHAT_HISTORY_MAX
from memory import get_relevant_memory, save_memory
from logger import get_logger

from tools.search     import web_search, search_news
from tools.pc_control import (open_application, list_files, take_screenshot,
                               get_system_info, copy_to_clipboard,
                               kill_process, get_top_processes)
from tools.email_tool import send_email
from tools.whatsapp   import send_whatsapp
from tools.monitor    import start_system_monitor, stop_system_monitor
from tools.reminder   import set_reminder, list_reminders, clear_reminders
from tools.calculator import calculate, convert_units, get_datetime_info

log = get_logger("brain")

_llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name=GROQ_MODEL,
    temperature=0,
    max_tokens=512,
)

ALL_TOOLS = [
    web_search, search_news,
    open_application, list_files, take_screenshot,
    get_system_info, copy_to_clipboard, kill_process, get_top_processes,
    send_email, send_whatsapp,
    start_system_monitor, stop_system_monitor,
    set_reminder, list_reminders, clear_reminders,
    calculate, convert_units, get_datetime_info,
]

BASE_SYSTEM = (
    "You are BUJJI, a smart personal AI assistant like JARVIS."
    " Call each tool EXACTLY ONCE. Never retry after getting a result."
    " open_application app_name must be one lowercase word only from:"
    " chrome firefox notepad calculator paint excel word powerpoint vscode"
    " terminal cmd explorer youtube gmail email whatsapp chatgpt github"
    " kaggle colab instagram twitter linkedin netflix google maps amazon"
    " flipkart spotify reddit stackoverflow discord notion."
    " open whatsapp / see whatsapp -> open_application app_name=whatsapp."
    " open email / gmail -> open_application app_name=gmail."
    " After any tool returns -> give Final Answer in 1-2 lines, stop."
    " Respond in same language as user: Hindi/English/Hinglish."
)

_agent = create_react_agent(_llm, ALL_TOOLS)
_chat_history = []


def ask_jarvis(user_input, emotion="neutral"):
    global _chat_history

    from tools.emotion import emotion_tone_hint
    tone    = emotion_tone_hint(emotion)
    mem_ctx = get_relevant_memory(user_input)

    system = BASE_SYSTEM
    if tone:
        system = system + " TONE: " + tone
    if mem_ctx:
        system = system + " PAST CONTEXT: " + mem_ctx

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
            answer = "Done, sir."

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
            return "Done, sir."
        if any(k in err for k in ["tool_use_failed", "Failed to call", "400", "tool call validation"]):
            return "Dobara clearly boliye - jaise open whatsapp ya open youtube."
        return "Error: " + err[:100]


def clear_history():
    global _chat_history
    _chat_history = []
    return "Chat history cleared."