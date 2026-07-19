try:
    from ddgs import DDGS
except ImportError:
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        DDGS = None


def get_live_news_context(sport_name):
    if DDGS is None:
        return "Live news unavailable: search package not installed."

    search_query = f"{sport_name} latest tournament results news 2026"
    retrieved_texts = []

    try:
        with DDGS() as ddgs:
            results = ddgs.text(search_query, max_results=3)
            for index, r in enumerate(results, start=1):
                title = r.get("title", "No Title")
                snippet = r.get("body", "No Snippet Content Available")
                retrieved_texts.append(f"Web Source {index}: {title}\nSnippet: {snippet}")
    except Exception as e:
        retrieved_texts.append(f"Live news unavailable: {e}")

    return "\n\n".join(retrieved_texts)
