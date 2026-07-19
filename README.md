# AI-Powered Sports Quiz Generation Agent

This project builds an AI agent that generates sports-related multiple-choice quizzes using Retrieval-Augmented Generation (RAG) with ChromaDB and web search.

## Setup

1. Create and activate a virtual environment:

```powershell
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

3. Create a `.env` file in the root folder with your OpenAI API key:

```text
OPENAI_API_KEY=your_api_key_here
```

4. Run the app:

```powershell
streamlit run app.py
```
