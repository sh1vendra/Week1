from sentence_transformers import SentenceTransformer
import chromadb
from ingest import chunk_documents

CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "professor_reviews"
EMBED_MODEL = "all-MiniLM-L6-v2"

_model = None
_collection = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)
    return _model


def _get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        _collection = client.get_or_create_collection(COLLECTION_NAME)
    return _collection


def build_index() -> None:
    collection = _get_collection()
    if collection.count() > 0:
        print(f"Collection already has {collection.count()} documents, skipping re-embed.")
        return

    chunks = chunk_documents()
    model = _get_model()
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    collection.add(
        ids=[f"{c['source']}_{c['chunk_index']}" for c in chunks],
        documents=texts,
        embeddings=embeddings,
        metadatas=[{"source": c["source"], "chunk_index": c["chunk_index"]} for c in chunks],
    )
    print(f"Indexed {len(chunks)} chunks into '{COLLECTION_NAME}'.")


def retrieve(query: str, k: int = 4) -> list[dict]:
    model = _get_model()
    collection = _get_collection()
    query_embedding = model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=k)
    output = []
    for text, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        output.append({
            "text": text,
            "source": metadata["source"],
            "distance": round(distance, 4),
        })
    return output


if __name__ == "__main__":
    build_index()

    queries = [
        "What do students say about Ted Lehr exams?",
        "Which math professor is easiest at Texas State?",
        "What is Professor Zong like for CS courses?",
    ]

    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 60)
        results = retrieve(query)
        for r in results:
            print(f"  Distance: {r['distance']}  |  Source: {r['source']}")
            print(f"  Text: {r['text'][:200]}")
            print()
