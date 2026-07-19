import os
import json
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHROMA_DB_PATH = PROJECT_ROOT / "chroma_db"
DEFAULT_FACTS_PATH = PROJECT_ROOT / "data" / "sports_facts.json"


def get_chroma_client():
    return chromadb.PersistentClient(path=str(CHROMA_DB_PATH))


def setup_and_populate_db(json_file_path=None):
    if json_file_path is None:
        json_file_path = DEFAULT_FACTS_PATH
    else:
        json_file_path = Path(json_file_path)
        if not json_file_path.is_absolute():
            json_file_path = PROJECT_ROOT / json_file_path

    client = get_chroma_client()
    embedding_fn = embedding_functions.DefaultEmbeddingFunction()

    collection = client.get_or_create_collection(
        name="sports_history",
        embedding_function=embedding_fn
    )

    if collection.count() > 0:
        return collection

    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"Raw fact data file not found at {json_file_path}")

    with open(json_file_path, "r", encoding="utf-8") as f:
        facts_list = json.load(f)

    documents = []
    metadata_list = []
    ids = []

    for idx, item in enumerate(facts_list):
        documents.append(item["fact"])
        metadata_list.append({"sport": item["sport"]})
        ids.append(f"fact_{idx}")

    collection.add(
        documents=documents,
        metadatas=metadata_list,
        ids=ids
    )
    return collection


def query_historic_facts(sport, query_text, n_results=3):
    client = get_chroma_client()
    embedding_fn = embedding_functions.DefaultEmbeddingFunction()
    collection = client.get_or_create_collection(
        name="sports_history",
        embedding_function=embedding_fn
    )

    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        where={"sport": sport}
    )

    return results.get("documents", [[]])[0]
