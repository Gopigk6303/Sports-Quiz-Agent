# Sports Quiz Agent

A lightweight Streamlit app that combines a local knowledge base with live search context to generate grounded sports quiz questions.

## Quick start

1. Create and activate a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your OpenAI API key if you want to use the live LLM generator.
4. Run the app: `streamlit run app.py`

## Project notes

- The app uses a local JSON knowledge base by default so it can run even when vector databases or external APIs are unavailable.
- If an OpenAI API key is present, the generator uses it; otherwise it falls back to a deterministic quiz template.
