try:
    from duckduckgo_search import DDGS
except Exception:  # pragma: no cover - optional dependency path
    DDGS = None


def get_live_news_context(sport_name):
    """Retrieve live web context for the chosen sport when available."""
    search_query = f"{sport_name} latest tournament results championship winners news 2026"

    if DDGS is None:
        return "No live search results available because the duckduckgo-search package is not installed."

    try:
        with DDGS() as ddgs:
            results = ddgs.text(search_query, max_results=3)
            snippets = []
            for index, result in enumerate(results, start=1):
                title = result.get("title", "No title")
                snippet = result.get("body", "No snippet available")
                snippets.append(f"Web Source {index}: {title}\nSnippet: {snippet}")
            return "\n\n".join(snippets) if snippets else "No recent search results were returned."
    except Exception as exc:  # pragma: no cover - network dependent
        return f"No recent search engine updates available due to connectivity: {exc}"
