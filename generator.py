import os
from dotenv import load_dotenv
from groq import Groq
from retriever import retrieve

load_dotenv()

GROQ_MODEL = "llama-3.3-70b-versatile"
SYSTEM_PROMPT = (
    "Answer using only the review text provided below. "
    "If the answer is not contained in the provided reviews, say so explicitly. "
    "Do not draw on outside knowledge about professors or courses."
)

_client = None


def _get_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(api_key=os.environ["GROQ_API_KEY"])
    return _client


def generate(question: str) -> dict:
    chunks = retrieve(question, k=4)

    context_blocks = []
    for i, chunk in enumerate(chunks, start=1):
        context_blocks.append(f"[{i}] Source: {chunk['source']}\n{chunk['text']}")
    context = "\n\n".join(context_blocks)

    user_message = f"Context:\n{context}\n\nQuestion: {question}"

    response = _get_client().chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    answer = response.choices[0].message.content
    sources = list(dict.fromkeys(chunk["source"] for chunk in chunks))

    return {"answer": answer, "sources": sources}


if __name__ == "__main__":
    questions = [
        "What do students say about Ted Lehr?",
        "Which math professor would you recommend for someone bad at math?",
        "What is the best restaurant in San Marcos?",
    ]

    for question in questions:
        print(f"\nQuestion: {question}")
        print("=" * 60)
        result = generate(question)
        print(f"Answer:\n{result['answer']}")
        print(f"\nSources: {result['sources']}")
        print()
