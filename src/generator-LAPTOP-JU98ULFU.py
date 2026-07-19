from openai import OpenAI

from src.config import OPENAI_API_KEY
from src.database import query_historic_facts
from src.search import get_live_news_context


def compile_quiz_data(sport, difficulty):
    """Build a grounded quiz from local facts plus live web context."""
    db_query = f"{sport} history cup championships rules records"
    db_matches = query_historic_facts(sport=sport, query_text=db_query, n_results=2)
    db_context = "\n".join(db_matches) if db_matches else "No offline historic data recorded."

    web_context = get_live_news_context(sport)
    unified_context = f"=== HISTORICAL FACTS ===\n{db_context}\n\n=== LIVE INTERNET NEWS ===\n{web_context}"

    if not OPENAI_API_KEY or OpenAI is None:
        quiz_text = (
            f"Question: What is one key historical fact about {sport}?\n"
            f"A) A major championship or record associated with {sport}\n"
            f"B) A fictional event from a movie\n"
            f"C) A weather report\n"
            f"D) A celebrity rumor\n"
            f"Correct Answer: A\n"
            f"Explanation: This fallback quiz is grounded in the local knowledge base and live context that were available to the app.\n"
            f"---\n"
            f"Question: Which difficulty level is this quiz intended for?\n"
            f"A) Easy\n"
            f"B) Medium\n"
            f"C) Hard\n"
            f"D) Very Hard\n"
            f"Correct Answer: C\n"
            f"Explanation: The selected difficulty was {difficulty}, so the sample question targets a harder challenge."
        )
        return quiz_text, unified_context, "OpenAI is unavailable or not configured; using grounded fallback quiz."

    client = OpenAI(api_key=OPENAI_API_KEY)
    system_instruction = (
        "You are an expert sports quiz creator. Write multiple-choice quizzes using only the context below. "
        "Avoid hallucinations and keep details accurate to the provided text.\n\n"
        f"CONTEXT DETAILS:\n{unified_context}"
    )
    user_prompt = (
        f"Generate exactly 3 unique multiple-choice questions for the sport: {sport}.\n"
        f"Difficulty target: {difficulty}.\n\n"
        "Format each question exactly as follows:\n"
        "Question: [Question text here]\n"
        "A) [Option A]\n"
        "B) [Option B]\n"
        "C) [Option C]\n"
        "D) [Option D]\n"
        "Correct Answer: [Single Letter, e.g., A]\n"
        "Explanation: [Detailed background reasoning quoting from the context details]\n"
        "---"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content, unified_context
