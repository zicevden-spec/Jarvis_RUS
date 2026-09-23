"""Этап 6: веб-поиск через DuckDuckGo, без ключей API."""
from ddgs import DDGS


def search(query: str, max_results: int = 3) -> str:
    with DDGS() as ddgs:
        results = list(ddgs.text(query, region="ru-ru", max_results=max_results))
    if not results:
        return "Ничего не нашёл в интернете по этому запросу."
    lines = []
    for r in results:
        title = r.get("title", "")
        body = r.get("body", "")
        lines.append(f"{title}: {body}")
    return "\n".join(lines)
