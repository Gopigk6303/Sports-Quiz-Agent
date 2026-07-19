import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def test_importing_generator_is_safe_without_openai_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "placeholder")
    sys.modules.pop("src.config", None)
    sys.modules.pop("src.generator", None)

    generator = importlib.import_module("src.generator")

    assert generator.OPENAI_API_KEY is None


def test_compile_quiz_data_uses_context_when_openai_unavailable(monkeypatch):
    generator = importlib.import_module("src.generator")

    monkeypatch.setattr(generator, "OpenAI", None)
    monkeypatch.setattr(generator, "OPENAI_API_KEY", None)

    quiz_text, context, error = generator.compile_quiz_data("Football", "Hard")

    assert "Football" in quiz_text
    assert "Hard" in quiz_text
    assert "HISTORICAL FACTS" in context or "LIVE INTERNET NEWS" in context
    assert error is not None


def test_setup_and_populate_db_uses_project_paths_when_cwd_changes(monkeypatch, tmp_path):
    from src import database

    class FakeCollection:
        def __init__(self):
            self.added = None

        def count(self):
            return 0

        def add(self, documents, metadatas, ids):
            self.added = (documents, metadatas, ids)

    class FakeClient:
        def __init__(self, path):
            self.path = path

        def get_or_create_collection(self, name, embedding_function):
            return FakeCollection()

    monkeypatch.setattr(database, "get_chroma_client", lambda: FakeClient("ignored"))
    monkeypatch.chdir(tmp_path)

    collection = database.setup_and_populate_db()

    assert collection.added is not None
    assert len(collection.added[0]) > 0
