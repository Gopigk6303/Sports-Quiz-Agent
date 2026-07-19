import os
from dotenv import load_dotenv

load_dotenv()


def _normalize_api_key(value):
    if value is None:
        return None

    normalized_value = value.strip()
    if not normalized_value:
        return None

    placeholder_values = {
        "your_openai_api_key_here",
        "your_api_key_here",
        "changeme",
        "placeholder",
    }

    if normalized_value.lower() in placeholder_values:
        return None

    return normalized_value


OPENAI_API_KEY = _normalize_api_key(os.getenv("OPENAI_API_KEY"))
