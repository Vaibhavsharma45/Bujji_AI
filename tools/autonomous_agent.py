"""
tools/autonomous_agent.py — BUJJI Autonomous Browser Agent
Uses Playwright to control browser, fill forms, scrape data, automate tasks.
This is the JARVIS-level feature — BUJJI can actually DO things on the web.
"""
import asyncio, json, os, threading
from langchain_core.tools import tool
from logger import get_logger

log = get_logger("tool.autonomous")


def _run_async(coro):
    """Run async coroutine from sync context safely."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = pool.submit(asyncio.run, coro)
                return future.result(timeout=60)
        return loop.run_until_complete(coro)
    except Exception:
        return asyncio.run(coro)


async def _do_web_research(query: str, max_pages: int = 3) -> str:
    try:
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # Google search
            await page.goto(f"https://www.google.com/search?q={query.replace(' ', '+')}")
            await page.wait_for_load_state("networkidle", timeout=10000)

            # Extract search results
            results = await page.query_selector_all("div.g")
            summaries = []
            for r in results[:max_pages]:
                try:
                    title = await r.query_selector("h3")
                    snippet = await r.query_selector("div.VwiC3b")
                    t = await title.inner_text() if title else ""
                    s = await snippet.inner_text() if snippet else ""
                    if t:
                        summaries.append(f"• {t}: {s[:200]}")
                except Exception:
                    pass

            await browser.close()
            return "\n".join(summaries) if summaries else "No results found."
    except ImportError:
        return "playwright install karo: pip install playwright && python -m playwright install chromium"
    except Exception as e:
        log.error(f"Web research error: {e}")
        return f"Research failed: {e}"


async def _do_fill_form(url: str, fields: dict) -> str:
    try:
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)  # visible so user can see
            page = await browser.new_page()
            await page.goto(url, timeout=15000)
            await page.wait_for_load_state("networkidle", timeout=10000)

            filled = []
            for selector, value in fields.items():
                try:
                    await page.fill(selector, value)
                    filled.append(selector)
                except Exception:
                    try:
                        await page.type(selector, value)
                        filled.append(selector)
                    except Exception:
                        pass

            result = f"Form pe {len(filled)} fields fill kiye: {', '.join(filled)}"
            # Keep browser open for user to verify
            await asyncio.sleep(3)
            await browser.close()
            return result
    except ImportError:
        return "pip install playwright && python -m playwright install chromium"
    except Exception as e:
        return f"Form fill failed: {e}"


async def _do_scrape_page(url: str) -> str:
    try:
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=15000)
            await page.wait_for_load_state("networkidle", timeout=10000)
            title = await page.title()
            # Get main text content
            content = await page.evaluate("""() => {
                const els = document.querySelectorAll('p, h1, h2, h3, li');
                return Array.from(els).map(e => e.innerText).filter(t => t.length > 20).slice(0, 30).join('\\n');
            }""")
            await browser.close()
            return f"Page: {title}\n\n{content[:1500]}"
    except ImportError:
        return "pip install playwright && python -m playwright install chromium"
    except Exception as e:
        return f"Scrape failed: {e}"


async def _do_youtube_search_play(query: str) -> str:
    try:
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.goto(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
            await page.wait_for_load_state("networkidle", timeout=10000)
            # Click first video
            first_video = await page.query_selector("ytd-video-renderer a#video-title")
            if first_video:
                title = await first_video.get_attribute("title") or "video"
                await first_video.click()
                await page.wait_for_load_state("networkidle", timeout=10000)
                return f"Playing on YouTube: {title}"
            await browser.close()
            return "Video nahi mila YouTube pe."
    except ImportError:
        return "pip install playwright && python -m playwright install chromium"
    except Exception as e:
        return f"YouTube error: {e}"


async def _do_browser_task(task: str) -> str:
    """Generic browser task using AI-guided steps."""
    task_lower = task.lower()
    try:
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()

            if "google" in task_lower or "search" in task_lower:
                query = task.replace("google", "").replace("search", "").strip()
                await page.goto(f"https://google.com/search?q={query.replace(' ', '+')}")
            elif "open" in task_lower:
                site = task_lower.replace("open", "").strip()
                await page.goto(f"https://{site}.com" if "http" not in site else site)
            elif "github" in task_lower:
                await page.goto("https://github.com")
            else:
                await page.goto(f"https://google.com/search?q={task.replace(' ', '+')}")

            await page.wait_for_load_state("networkidle", timeout=10000)
            title = await page.title()
            await asyncio.sleep(2)
            # Don't close — user can interact
            return f"Browser task done: {title}"
    except ImportError:
        return "pip install playwright && python -m playwright install chromium"
    except Exception as e:
        return f"Browser task failed: {e}"


# ── Sync tool wrappers ─────────────────────────────────────────────────────────

@tool
def autonomous_web_research(query: str) -> str:
    """
    Autonomously research any topic on the web using real browser.
    Opens browser, searches Google, extracts and summarizes top results.
    Use for: latest news, detailed research, fact checking, current data.
    """
    log.info(f"Autonomous research: {query}")
    return _run_async(_do_web_research(query))


@tool
def autonomous_youtube_play(query: str) -> str:
    """
    Autonomously open YouTube and play a specific video or song.
    Opens real browser, searches YouTube, clicks and plays the first result.
    Use when user says: play X on youtube, youtube pe X chalao.
    """
    log.info(f"YouTube play: {query}")
    return _run_async(_do_youtube_search_play(query))


@tool
def autonomous_scrape_website(url: str) -> str:
    """
    Autonomously visit a website and extract its content.
    Returns title and main text content from any webpage.
    Use for: reading articles, checking website content, extracting data.
    """
    log.info(f"Scraping: {url}")
    return _run_async(_do_scrape_page(url))


@tool
def autonomous_browser_task(task: str) -> str:
    """
    Autonomously perform any browser task described in plain language.
    Examples: 'open github profile', 'google latest AI news', 'search flipkart phones'.
    Opens a real visible browser and performs the task.
    """
    log.info(f"Browser task: {task}")
    return _run_async(_do_browser_task(task))


@tool
def autonomous_fill_form(url: str, form_data: str) -> str:
    """
    Autonomously fill a web form. 
    url: the webpage URL with the form.
    form_data: JSON string of CSS selectors to values, e.g. '{"#name": "Vaibhav", "#email": "v@gmail.com"}'.
    """
    log.info(f"Fill form: {url}")
    try:
        fields = json.loads(form_data)
    except Exception:
        return "form_data must be valid JSON like: {\"#name\": \"Vaibhav\"}"
    return _run_async(_do_fill_form(url, fields))