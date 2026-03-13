from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
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

SYSTEM_MESSAGE = """You are BUJJI, a smart AI assistant.

TOOL CALLING RULES — STRICTLY FOLLOW:
- open_application ka app_name SIRF in values mein se ek hona chahiye:
  chrome, whatsapp, youtube, chatgpt, gmail, github, spotify, notepad,
  calculator, vscode, kaggle, colab, instagram, twitter, linkedin,
  netflix, google, maps, openai, dailymotion, amazon, flipkart
- Koi bhi "open X" command aaye — seedha open_application(app_name="X") call karo
- app_name mein spaces nahi, sirf lowercase single word
- web search ke liye web_search tool use karo
- Response 1-2 lines max, same language mein jo user ne boli

EXAMPLES:
- "open youtube" → open_application(app_name="youtube")
- "youtube kholo" → open_application(app_name="youtube")  
- "search AI news" → web_search(query="AI news")
- "system info" → get_system_info()"""

agent = create_react_agent(llm, tools)
chat_history = []

def ask_jarvis(user_input: str) -> str:
    global chat_history

    memory_context = get_relevant_memory(user_input)
    system_content = SYSTEM_MESSAGE
    if memory_context:
        system_content += f"\n\nPast context:\n{memory_context}"

    messages = ([SystemMessage(content=system_content)]
                + chat_history[-6:]
                + [HumanMessage(content=user_input)])

    try:
        response = agent.invoke({"messages": messages})
        answer = ""
        for msg in reversed(response["messages"]):
            if hasattr(msg, "content") and msg.content and msg.type == "ai":
                answer = msg.content
                break

        if not answer:
            answer = "Dobara boliye sir."

        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=answer))
        save_memory(user_input, answer)
        return answer

    except Exception as e:
        err = str(e)
        if "tool_use_failed" in err or "Failed to call" in err:
            return "Tool call fail hua. Thoda alag tarike se boliye — jaise 'open youtube' ya 'search AI news'."
        return f"Error: {err}"