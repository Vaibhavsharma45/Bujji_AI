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

SYSTEM_MESSAGE = """You are BUJJI, a smart personal AI assistant for your user.

STRICT RULES — follow exactly:
1. "open X" command aaye toh SIRF open_application("X") call karo. Koi explanation nahi.
2. open_application mein app_name SIRF ek word hona chahiye: "youtube", "whatsapp", "chrome", "chatgpt", "gmail" etc.
3. Search ke liye web_search tool use karo.
4. Har response Hindi ya English mein do — jis bhasha mein user bola.
5. Response short rakho — 1-2 lines max.
6. Agar kuch samajh na aaye toh poochho mat — best guess lagao aur karo.

Available apps to open: chrome, whatsapp, youtube, chatgpt, openai, gmail, github, spotify, notepad, calculator, vscode, kaggle, colab, instagram, twitter, linkedin, netflix, google, maps"""

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
        for msg in reversed(response["messages"]):
            if hasattr(msg, "content") and msg.content and msg.type == "ai":
                answer = msg.content
                break
        else:
            answer = "Dobara boliye."

        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=answer))
        save_memory(user_input, answer)
        return answer

    except Exception as e:
        return f"Error: {str(e)}"