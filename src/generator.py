from src.config import OPENAI_API_KEY
from src.database import query_historic_facts
from src.search import get_live_news_context

try:
    from openai import OpenAI
    from openai import APIStatusError, RateLimitError
except Exception:  # pragma: no cover - optional dependency path
    OpenAI = None
    APIStatusError = RateLimitError = Exception


def compile_quiz_data(sport, difficulty, request_id=None):
    db_query = f"{sport} history cup championships rules records"
    db_matches = query_historic_facts(sport=sport, query_text=db_query, n_results=2)
    db_context = "\n".join(db_matches) if db_matches else "No offline historic data recorded."

    fallback_web_context = "Live news unavailable: skipped because OpenAI API key is missing or invalid."
    unified_context = f"=== HISTORICAL FACTS ===\n{db_context}\n\n=== LIVE INTERNET NEWS ===\n{fallback_web_context}"

    fallback_quiz = (
        f"Question: What is one key historical fact about {sport}?\n"
        f"A) A major championship or record associated with {sport}\n"
        f"B) A fictional event from a movie\n"
        f"C) A weather report\n"
        f"D) A celebrity rumor\n"
        f"Correct Answer: A\n"
        f"Explanation: This fallback quiz is grounded in the local knowledge base and available search context.\n"
        f"---\n"
        f"Question: Which difficulty level is this quiz intended for?\n"
        f"A) Easy\n"
        f"B) Medium\n"
        f"C) Hard\n"
        f"D) Very Hard\n"
        f"Correct Answer: C\n"
        f"Explanation: The selected difficulty was {difficulty}, so the sample question targets a harder challenge."
    )

    if not OPENAI_API_KEY or OpenAI is None or OPENAI_API_KEY.lower().startswith(("your", "changeme", "placeholder")):
        return fallback_quiz, unified_context, "OpenAI is unavailable or not configured; using grounded fallback quiz."

    web_context = get_live_news_context(sport)
    unified_context = f"=== HISTORICAL FACTS ===\n{db_context}\n\n=== LIVE INTERNET NEWS ===\n{web_context}"

    client = OpenAI(api_key=OPENAI_API_KEY)

    system_instruction = (
        "You are an expert sports quiz creator. Use only the facts in the provided Context. "
        "Do not hallucinate or invent details outside the text. If facts are limited, make questions that remain accurate.\n\n"
        f"CONTEXT DETAILS:\n{unified_context}"
    )

    user_prompt = (
        f"Generate exactly 3 unique multiple-choice questions for the sport: {sport}.\n"
        f"Difficulty target: {difficulty}.\n"
        f"Generation request id: {request_id or 'default'}.\n"
        "Make the questions feel fresh and different from any earlier set while staying grounded in the context.\n\n"
        "Format each question exactly as follows for parsing:\n"
        "Question: [Question text here]\n"
        "A) [Option A]\n"
        "B) [Option B]\n"
        "C) [Option C]\n"
        "D) [Option D]\n"
        "Correct Answer: [Single Letter]\n"
        "Explanation: [Accurate explanation based on the context text].\n"
        "---\n"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=750
        )
        return response.choices[0].message.content, unified_context, None
    except (RateLimitError, APIStatusError, Exception):
        error_msg = "OpenAI is currently unavailable; using grounded fallback quiz."
        return fallback_quiz, unified_context, error_msg
