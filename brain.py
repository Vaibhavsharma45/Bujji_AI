from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from config import GROQ_API_KEY, GROQ_MODEL
from tools.search import web_search
from tools.pc_control import open_application, list_files, take_screenshot, get_system_info
from tools.email_tool import send_email
from tools.whatsapp import send_whatsapp
from memory import get_relevant_memory, save_memory

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name=GROQ_MODEL,
    temperature=0,
)

tools = [
    web_search,
    open_application,
    list_files,
    take_screenshot,
    get_system_info,
    send_email,
    send_whatsapp,
]

SYSTEM_MESSAGE = """You are BUJJI, a smart personal AI assistant.
You have tools to control the PC, search the web, send emails and WhatsApp messages.

IMPORTANT RULES:
- When user says "open X" — use open_application tool immediately. Do NOT explain, just call the tool.
- When user asks to search something — use web_search tool.
- When user says "send email" — use send_email tool.
- When user says "send whatsapp" — use send_whatsapp tool.
- Always respond in the same language the user used (Hindi or English).
- Keep responses short and to the point.
- Do NOT return raw function syntax in your response. Use tools properly."""

agent = create_react_agent(llm, tools)
chat_history = []

def ask_jarvis(user_input: str) -> str:
    global chat_history

    memory_context = get_relevant_memory(user_input)
    system_content = SYSTEM_MESSAGE
    if memory_context:
        system_content += f"\n\nPast context:\n{memory_context}"

    messages = [SystemMessage(content=system_content)] + chat_history[-6:] + [HumanMessage(content=user_input)]

    try:
        response = agent.invoke({"messages": messages})
        # Last AI message nikalo
        for msg in reversed(response["messages"]):
            if hasattr(msg, "content") and msg.content and msg.type == "ai":
                answer = msg.content
                break
        else:
            answer = "Kuch samajh nahi aaya, dobara boliye."

        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=answer))
        save_memory(user_input, answer)
        return answer

    except Exception as e:
        return f"Error: {str(e)}"