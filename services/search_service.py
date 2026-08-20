"""
Web Search service using DuckDuckGo with fast timeout fallback for real-time IDP IELTS updates.
"""
import logging
import asyncio
from ddgs import DDGS

logger = logging.getLogger(__name__)

async def search_web_async(query: str, max_results: int = 3, lang: str = "uz") -> list[dict]:
    """
    Asynchronous fast web search with 3-second timeout protection.
    """
    def _sync_search():
        results = []
        try:
            with DDGS(timeout=3) as ddgs:
                raw_results = ddgs.text(query, max_results=max_results)
                for item in raw_results:
                    title = item.get("title", "").strip()
                    href = item.get("href", "").strip()
                    body = item.get("body", "").strip()
                    if title and href:
                        results.append({
                            "title": title,
                            "url": href,
                            "snippet": body
                        })
        except Exception as e:
            logger.debug(f"Fast search notice for query '{query}': {e}")
        return results

    loop = asyncio.get_running_loop()
    try:
        return await asyncio.wait_for(loop.run_in_executor(None, _sync_search), timeout=3.5)
    except Exception:
        return []

def format_search_results(query: str, results: list[dict], lang: str = "uz") -> str:
    if not results:
        if lang == "uz":
            return f"🔍 *Qidiruv natijasi topilmadi:*\n`{query}` bo'yicha ma'lumot topilmadi. Iltimos boshqa kalit so'zlarni kiriting."
        elif lang == "ru":
            return f"🔍 *Результаты поиска не найдены:*\nПо запросу `{query}` ничего не найдено. Пожалуйста, попробуйте изменить формулировку."
        else:
            return f"🔍 *No search results found:*\nNothing found for `{query}`. Please try different keywords."

    if lang == "uz":
        header = f"🌐 *'{query}' bo'yicha qidiruv natijalari:*\n\n"
    elif lang == "ru":
        header = f"🌐 *Результаты онлайн поиска по запросу '{query}':*\n\n"
    else:
        header = f"🌐 *Web Search Results for '{query}':*\n\n"

    items = []
    for i, res in enumerate(results, 1):
        title = res["title"].replace("*", "").replace("[", "(").replace("]", ")")
        snippet = res["snippet"].replace("*", "").replace("[", "(").replace("]", ")")
        url = res["url"]
        item_text = f"{i}. 🔗 *[{title}]({url})*\n_{snippet}_\n"
        items.append(item_text)

    footer = f"\n💡 _Batafsil ma'lumot uchun havolalar ustiga bosing._" if lang == "uz" else (
        f"\n💡 _Нажмите на ссылку для перехода к первоисточнику._" if lang == "ru" else
        f"\n💡 _Click on the links above for full information._"
    )

    return header + "\n".join(items) + footer
