from langchain_core.tools import tool
from ddgs import DDGS
from logger import get_logger

log = get_logger("tool.search")


@tool
def web_search(query: str) -> str:
    """Search the web for any current information, news, facts, prices, or events."""
    log.info(f"Web search: {query}")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
        if not results:
            return "No search results found."
        lines = [f"• {r.get('title', '')}: {r.get('body', '')[:200]}" for r in results]
        return "\n".join(lines)
    except Exception as e:
        log.error(f"Search failed: {e}")
        return f"Search unavailable: {e}"


@tool
def search_news(topic: str) -> str:
    """Search for latest news on any topic."""
    log.info(f"News search: {topic}")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news(topic, max_results=5))
        if not results:
            return "No news found."
        lines = [
            f"• [{r.get('date','?')[:10]}] {r.get('title','')}: {r.get('body','')[:150]}"
            for r in results
        ]
        return "\n".join(lines)
    except Exception as e:
        log.error(f"News search failed: {e}")
        return f"News unavailable: {e}"