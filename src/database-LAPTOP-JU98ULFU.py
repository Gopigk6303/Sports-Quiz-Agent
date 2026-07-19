import json
import os

try:
    import chromadb
    from chromadb.utils import embedding_functions
except Exception:  # pragma: no cover - optional dependency path
    chromadb = None
    embedding_functions = None


def get_chroma_client():
    """Initialize a persistent ChromaDB client if the dependency is available."""
    if chromadb is None:
        return None
    return chromadb.PersistentClient(path="./chroma_db")


def setup_and_populate_db(json_file_path="./data/sports_facts.json"):
    """Read local sports facts and populate the vector store when possible."""
    client = get_chroma_client()
    if client is None or embedding_functions is None:
        return None

    embedding_fn = embedding_functions.DefaultEmbeddingFunction()
    collection = client.get_or_create_collection(name="sports_history", embedding_function=embedding_fn)

    if collection.count() > 0:
        return collection

    if not os.path.exists(json_file_path):
        return collection

    with open(json_file_path, "r", encoding="utf-8") as handle:
        facts_list = json.load(handle)

    documents = []
    metadata_list = []
    ids = []

    for index, item in enumerate(facts_list):
        documents.append(item["fact"])
        metadata_list.append({"sport": item["sport"]})
        ids.append(f"fact_{index}")

    collection.add(documents=documents, metadatas=metadata_list, ids=ids)
    return collection


def query_historic_facts(sport, query_text, n_results=2):
    """Query the local collection for relevant historical facts."""
    client = get_chroma_client()
    if client is None or embedding_functions is None:
        return []

    embedding_fn = embedding_functions.DefaultEmbeddingFunction()
    collection = client.get_or_create_collection(name="sports_history", embedding_function=embedding_fn)

    results = collection.query(query_texts=[query_text], n_results=n_results, where={"sport": sport})
    return results.get("documents", [[]])[0]
