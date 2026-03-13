from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
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
    temperature=0.7,
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

SYSTEM_MESSAGE = """You are BUJJI, an advanced AI assistant — just like Iron Man's BUJJI.
You are helpful, intelligent, witty, and proactive. You speak in a friendly but professional tone.
You have access to powerful tools: web search, PC control, email, WhatsApp, and more.
Always be concise and helpful. Address the user as 'sir' occasionally for the BUJJI feel."""

agent = create_react_agent(llm, tools)

chat_history = []

def ask_bujji(user_input: str) -> str:
    global chat_history

    memory_context = get_relevant_memory(user_input)

    system_content = SYSTEM_MESSAGE
    if memory_context:
        system_content += f"\n\nRelevant past context:\n{memory_context}"

    messages = [SystemMessage(content=system_content)] + chat_history[-10:] + [HumanMessage(content=user_input)]

    try:
        response = agent.invoke({"messages": messages})
        answer = response["messages"][-1].content

        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=answer))

        save_memory(user_input, answer)
        return answer
    except Exception as e:
        return f"Something went wrong: {str(e)}"