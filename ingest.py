import os
import re

DOCS_DIR = "documents"
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50
MIN_CHUNK_LEN = 50


def load_documents(docs_dir: str = DOCS_DIR) -> list[dict]:
    docs = []
    for fname in sorted(os.listdir(docs_dir)):
        if not fname.endswith(".txt"):
            continue
        path = os.path.join(docs_dir, fname)
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
        cleaned = clean_text(raw)
        docs.append({"text": cleaned, "source": fname})
    return docs


def clean_text(text: str) -> str:
    lines = text.splitlines()
    lines = [line.strip() for line in lines if line.strip()]
    text = " ".join(lines)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def chunk_documents(docs_dir: str = DOCS_DIR) -> list[dict]:
    docs = load_documents(docs_dir)
    chunks = []
    for doc in docs:
        text = doc["text"]
        source = doc["source"]
        start = 0
        idx = 0
        while start < len(text):
            end = start + CHUNK_SIZE
            chunk_text = text[start:end].strip()
            if len(chunk_text) >= MIN_CHUNK_LEN:
                chunks.append({
                    "text": chunk_text,
                    "source": source,
                    "chunk_index": idx,
                })
                idx += 1
            start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


if __name__ == "__main__":
    chunks = chunk_documents()
    print(f"Total chunks: {len(chunks)}\n")
    print("--- 5 Sample Chunks ---\n")
    step = max(1, len(chunks) // 5)
    samples = [chunks[i * step] for i in range(5)]
    for chunk in samples:
        print(f"Source: {chunk['source']}  |  Index: {chunk['chunk_index']}")
        print(f"Text: {chunk['text']}")
        print()
