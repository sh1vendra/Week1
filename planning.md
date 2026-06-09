# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

Texas State University professor and course reviews collected from Rate My Professors. This knowledge is valuable because official university sources provide no information about actual exam difficulty, grading styles, or what study strategies work for specific professors. Students rely on peer knowledge to make informed course selection decisions.

---

## Documents

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | prof_ted_lehr_computer_science.txt | CS professor reviews | ratemyprofessors.com |
| 2 | prof_ziliang_zong_computer_science.txt | CS professor reviews | ratemyprofessors.com |
| 3 | prof_ellen_couvillion_mathematics.txt | Math professor reviews | ratemyprofessors.com |
| 4 | prof_john_burke_political_science.txt | Political Science reviews | ratemyprofessors.com |
| 5 | prof_david_johnson_biology.txt | Biology professor reviews | ratemyprofessors.com |
| 6 | prof_marla_burns_exercise_sport_health_ed.txt | Exercise Science reviews | ratemyprofessors.com |
| 7 | prof_shuying_sun_mathematics.txt | Math professor reviews | ratemyprofessors.com |
| 8 | prof_bobbie_moore_fashion_merchandising.txt | Fashion Merchandising reviews | ratemyprofessors.com |
| 9 | prof_jackson_rebrovich_mathematics.txt | Math professor reviews | ratemyprofessors.com |
| 10 | prof_edwin_vargas_computer_science.txt | CS professor reviews | ratemyprofessors.com |

---

## Chunking Strategy

**Chunk size:** 300 characters

**Overlap:** 50 characters

**Reasoning:** Reviews are short self-contained opinions, typically 2-4 sentences. 300 characters captures one complete review without merging unrelated opinions. Overlap of 50 characters prevents key information from being split across chunk boundaries. Chunks smaller than 100 characters lose the context that makes a review meaningful. Chunks larger than 600 characters merge multiple reviews and dilute retrieval precision.

---

## Retrieval Approach

**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers (local, no API key required)

**Top-k:** 4

**Production tradeoff reflection:** text-embedding-3-small (OpenAI) offers higher accuracy but costs money and adds API latency. multilingual-e5-base would be needed for multilingual student reviews. For a university with international students, multilingual support would matter significantly. Local model wins here for zero latency, no cost, and no rate limits during development.

---

## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say about Ted Lehr's teaching style? | Harsh, calls on students, grades based on favoritism, disrespects students |
| 2 | Which math professor is best for students who struggle with math? | Ellen Couvillion, reviews say she makes math easy and understandable |
| 3 | Is Edwin Vargas recommended for CS 1308? | No, reviews say class is not actually intro level, goes deep into AI |
| 4 | What do students say about Ziliang Zong? | Specific details from his reviews about teaching style and courses |
| 5 | Which professor has the best reviews overall at Texas State? | Ellen Couvillion or Marla Burns based on 5.0 ratings in documents |

---

## Anticipated Challenges

1. Professor nicknames or shortened names may not match full names in documents, causing retrieval misses on informal queries.

2. Reviews from different semesters may contradict each other with no timestamp metadata to resolve which is more recent or relevant.

---

## Architecture

```
Document Ingestion (.txt files in /documents)
        ↓
Chunking (300 char, 50 overlap) — ingest.py
        ↓
Embedding (all-MiniLM-L6-v2) + ChromaDB — retriever.py
        ↓
Retrieval (top-k=4)
        ↓
Groq LLM (llama-3.3-70b-versatile) — generator.py
        ↓
Gradio UI — app.py
```

---

## AI Tool Plan

**Milestone 3 — Ingestion and chunking:** Used Claude Code, provided document structure and chunking strategy section, asked it to implement chunk_documents() with 300 char size and 50 char overlap. Verified by checking chunk count (72) and printing 5 sample chunks.

**Milestone 4 — Embedding and retrieval:** Used Claude Code, provided retrieval approach section and architecture diagram, asked it to implement embed_and_store() and retrieve() using ChromaDB and all-MiniLM-L6-v2. Verified by running 3 test queries and checking distance scores.

**Milestone 5 — Generation and interface:** Used Claude Code, provided exact grounding prompt requirement and interface spec, asked it to implement generate() and Gradio UI. Verified grounding by testing off-topic refusal behavior.
