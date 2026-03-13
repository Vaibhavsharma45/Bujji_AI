from duckduckgo_search import DDGS
from langchain_core.tools import tool

@tool
def web_search(query: str) -> str:
    """Search the web for any current information, news, or facts."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=4))
        if not results:
            return "No results found."
        output = ""
        for r in results:
            output += f"- {r['title']}: {r['body']}\n"
        return output
    except Exception as e:
        return f"Search failed: {str(e)}"