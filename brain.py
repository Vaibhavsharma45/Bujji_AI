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

STRICT RULES:
1. Har tool sirf EK BAAR call karo. Kabhi retry mat karo.
2. Tool call ke baad seedha Final Answer do.
3. open_application ka app_name SIRF yeh values:
   chrome, whatsapp, youtube, chatgpt, gmail, github, spotify,
   notepad, calculator, vscode, kaggle, colab, instagram, twitter,
   linkedin, netflix, google, maps, openai, dailymotion, amazon, flipkart
4. "open email" ya "email open karo" = open_application(app_name="gmail") — SIRF EK BAAR
5. "send email" = send_email tool use karo
6. Response 1-2 lines max, same language mein jo user ne boli
7. Agar tool successful return kare — bas confirm karo, loop mat karo"""

agent = create_react_agent(
    llm,
    tools,
    prompt=SYSTEM_MESSAGE
)
chat_history = []

def ask_jarvis(user_input: str) -> str:
    global chat_history

    memory_context = get_relevant_memory(user_input)
    system_content = SYSTEM_MESSAGE
    if memory_context:
        system_content += f"\n\nPast context:\n{memory_context}"

    messages = (
        [SystemMessage(content=system_content)]
        + chat_history[-6:]
        + [HumanMessage(content=user_input)]
    )

    try:
        response = agent.invoke(
            {"messages": messages},
            config={"recursion_limit": 5}  # Max 5 steps — loop rok dega
        )
        answer = ""
        for msg in reversed(response["messages"]):
            if hasattr(msg, "content") and msg.content and msg.type == "ai":
                answer = msg.content
                break

        if not answer:
            answer = "Ho gaya sir."

        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=answer))
        save_memory(user_input, answer)
        return answer

    except Exception as e:
        err = str(e)
        if "recursion" in err.lower():
            return "Ho gaya sir."
        if "tool_use_failed" in err or "Failed to call" in err:
            return "Thoda alag tarike se boliye — jaise 'open gmail' ya 'search karo'."
        return f"Error: {err}"