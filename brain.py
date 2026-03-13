from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

from config import GROQ_API_KEY, GROQ_MODEL, JARVIS_NAME
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

SYSTEM_PROMPT = """You are JARVIS, an advanced AI assistant — just like Iron Man's JARVIS.
You are helpful, intelligent, witty, and proactive. You speak in a friendly but professional tone.
You have access to powerful tools: web search, PC control, email, WhatsApp, and more.

Relevant past memories:
{memory_context}

Tools available:
{tools}

Tool names: {tool_names}

Always think step by step using this format:
Question: the user's request
Thought: what should I do?
Action: the tool to use
Action Input: the input to the tool
Observation: the result
... (repeat if needed)
Thought: I now have the final answer
Final Answer: your response to the user

Begin!

Conversation so far:
{chat_history}

Question: {input}
Thought: {agent_scratchpad}"""

prompt = PromptTemplate(
    input_variables=["input", "agent_scratchpad", "chat_history", "memory_context", "tools", "tool_names"],
    template=SYSTEM_PROMPT,
)

memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    k=10,
    return_messages=False
)

agent        = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5,
)

def ask_jarvis(user_input: str) -> str:
    memory_context = get_relevant_memory(user_input) or "No relevant past context."
    try:
        response = agent_executor.invoke({
            "input": user_input,
            "memory_context": memory_context,
        })
        answer = response.get("output", "I couldn't process that.")
        save_memory(user_input, answer)
        return answer
    except Exception as e:
        return f"Something went wrong: {str(e)}"