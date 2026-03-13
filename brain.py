"""
brain.py — BUJJI's LangGraph ReAct Agent
Emotion-aware system prompt, persistent memory injection, 6-step limit.
"""
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.prebuilt import create_react_agent

from config import GROQ_API_KEY, GROQ_MODEL, GROQ_TEMP, GROQ_MAX_TOKENS, AGENT_RECURSION_LIMIT, CHAT_HISTORY_MAX
from memory import get_relevant_memory, save_memory
from logger import get_logger

# ── Tool imports ───────────────────────────────────────────────────────────────
from tools.search     import web_search, search_news
from tools.pc_control import (open_application, list_files, take_screenshot,
                              get_system_info, copy_to_clipboard, kill_process, get_top_processes)
from tools.email_tool import send_email
from tools.whatsapp   import send_whatsapp
from tools.monitor    import start_system_monitor, stop_system_monitor
from tools.reminder   import set_reminder, list_reminders, clear_reminders
from tools.calculator import calculate, convert_units, get_datetime_info

log = get_logger("brain")

# ── LLM setup ─────────────────────────────────────────────────────────────────
_llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name=GROQ_MODEL,
    temperature=GROQ_TEMP,
    max_tokens=GROQ_MAX_TOKENS,
)

ALL_TOOLS = [
    web_search, search_news,
    open_application, list_files, take_screenshot,
    get_system_info, copy_to_clipboard, kill_process, get_top_processes,
    send_email,
    send_whatsapp,
    start_system_monitor, stop_system_monitor,
    set_reminder, list_reminders, clear_reminders,
    calculate, convert_units, get_datetime_info,
]

_agent = create_react_agent(_llm, ALL_TOOLS)

BASE_SYSTEM = """You are BUJJI — a sharp, intelligent personal AI assistant like JARVIS from Iron Man.

STRICT RULES (violating these breaks the system):
1. Call every tool EXACTLY ONCE per request. Never call the same tool twice.
2. After any tool returns a result → give your Final Answer immediately. Stop.
3. open_application: app_name must be exactly one of these words (no spaces, lowercase):
   chrome firefox notepad calculator paint excel word powerpoint vscode terminal cmd
   explorer youtube gmail email whatsapp chatgpt github kaggle colab instagram twitter
   linkedin netflix google maps amazon flipkart spotify reddit stackoverflow discord notion
4. "open email" / "email kholo" → open_application(app_name="gmail") — ONCE only.
5. For math: use calculate tool. For unit conversion: use convert_units.
6. For time/date: use get_datetime_info.
7. Responses: 1-2 sentences max. Match the user's language (Hindi / English / Hinglish).
8. Be confident and direct — no filler, no "I think", no "maybe"."""


# ── State ──────────────────────────────────────────────────────────────────────
_chat_history: list = []


def ask_jarvis(user_input: str, emotion: str = "neutral") -> str:
    """
    Process a user command and return BUJJI's response.
    emotion: detected emotion from voice analysis (influences tone hint in prompt).
    """
    global _chat_history

    # Build dynamic system prompt
    from tools.emotion import emotion_tone_hint
    tone    = emotion_tone_hint(emotion)
    mem_ctx = get_relevant_memory(user_input)

    system  = BASE_SYSTEM
    if tone:
        system += f"\n\nTONE: {tone}"
    if mem_ctx:
        system += f"\n\nRELEVANT PAST CONTEXT:\n{mem_ctx}"

    messages = (
        [SystemMessage(content=system)]
        + _chat_history[-CHAT_HISTORY_MAX:]
        + [HumanMessage(content=user_input)]
    )

    log.info(f"Query → {user_input[:80]} (emotion={emotion})")

    try:
        result = _agent.invoke(
            {"messages": messages},
            config={"recursion_limit": AGENT_RECURSION_LIMIT},
        )

        # Extract the last AI message
        answer = ""
        for msg in reversed(result["messages"]):
            if getattr(msg, "type", "") == "ai" and msg.content and msg.content.strip():
                answer = msg.content.strip()
                break

        if not answer:
            answer = "Done, sir."

        # Update history
        _chat_history.append(HumanMessage(content=user_input))
        _chat_history.append(AIMessage(content=answer))
        if len(_chat_history) > CHAT_HISTORY_MAX:
            _chat_history = _chat_history[-CHAT_HISTORY_MAX:]

        save_memory(user_input, answer, emotion)
        log.info(f"Response → {answer[:80]}")
        return answer

    except Exception as e:
        err = str(e)
        log.error(f"Agent error: {err}")

        if "recursion" in err.lower():
            return "Ho gaya sir."
        if any(k in err for k in ["tool_use_failed", "Failed to call", "400"]):
            return "Thoda alag tarike se boliye — jaise 'open gmail' ya 'calculate 25% of 4000'."
        return f"Error: {err[:100]}"


def clear_history() -> str:
    global _chat_history
    _chat_history = []
    return "Chat history cleared."