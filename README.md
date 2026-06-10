# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

Texas State University professor and course reviews collected from Rate My Professors. This knowledge is valuable because official university sources provide no information about actual exam difficulty, grading styles, attendance policies, or what study strategies work for specific professors. Students rely on peer knowledge to make informed course selection decisions. This RAG system makes that informal knowledge searchable and answerable.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | prof_ted_lehr_computer_science.txt | RateMyProfessors reviews | documents/prof_ted_lehr_computer_science.txt |
| 2 | prof_ziliang_zong_computer_science.txt | RateMyProfessors reviews | documents/prof_ziliang_zong_computer_science.txt |
| 3 | prof_ellen_couvillion_mathematics.txt | RateMyProfessors reviews | documents/prof_ellen_couvillion_mathematics.txt |
| 4 | prof_john_burke_political_science.txt | RateMyProfessors reviews | documents/prof_john_burke_political_science.txt |
| 5 | prof_david_johnson_biology.txt | RateMyProfessors reviews | documents/prof_david_johnson_biology.txt |
| 6 | prof_marla_burns_exercise_sport_health_ed.txt | RateMyProfessors reviews | documents/prof_marla_burns_exercise_sport_health_ed.txt |
| 7 | prof_shuying_sun_mathematics.txt | RateMyProfessors reviews | documents/prof_shuying_sun_mathematics.txt |
| 8 | prof_bobbie_moore_fashion_merchandising.txt | RateMyProfessors reviews | documents/prof_bobbie_moore_fashion_merchandising.txt |
| 9 | prof_jackson_rebrovich_mathematics.txt | RateMyProfessors reviews | documents/prof_jackson_rebrovich_mathematics.txt |
| 10 | prof_edwin_vargas_computer_science.txt | RateMyProfessors reviews | documents/prof_edwin_vargas_computer_science.txt |

---

## Chunking Strategy

**Chunk size:** 300 characters

**Overlap:** 50 characters

**Why these choices fit your documents:** Reviews are short self-contained opinions, typically 2-4 sentences long. 300 characters captures one complete review without merging unrelated opinions from different students. Overlap of 50 characters prevents key information from being split across chunk boundaries. Chunks smaller than 100 characters lose the surrounding context that makes a review meaningful. Chunks larger than 600 characters merge multiple reviews and dilute retrieval precision since each chunk would match too many different queries.

**Final chunk count:** 72

---

## Sample Chunks

Chunk 1 (source: prof_bobbie_moore_fashion_merchandising.txt):
> Professor: Bobbie Moore | Course: MGT4378 | Rating: 5.0/5 | Difficulty: 2.0/5 "Professor Moore really cares about training and her students, the class surrounds a semester long group project. Make sure you have a good group and an interesting topic because it will effect your enjoyment of the class.

Chunk 2 (source: prof_david_johnson_biology.txt):
> Take notes!!!" Professor: David Johnson | Course: BIO1330 | Rating: 1.0/5 | Difficulty: 5.0/5 "BRUHHHHH. this class ABSOLUTELY SUCKED. I had to teach myself how to do everything the whole time. People around me didn't even know what this guy was talking abt. I barely passed this class and was guessi

Chunk 3 (source: prof_ellen_couvillion_mathematics.txt):
> math professor if you're nervous to take algebra. Lectures are easy to understand with a note packet done in class. Gives test reviews really similar to tests. Tests are sometimes easier than you think. Uses tophat in class for attendance points, drops 5 tophats (basically can get 5 absences) Very c

Chunk 4 (source: prof_john_burke_political_science.txt):
> .0/5 "Do not take him unless you want to sit there and be confused, he gets off topic a lot and he does not do reviews. He uses Key concepts and more than half of the concepts aren't on the exam. Attendance is not mandatory but if you do not attend you will barley pass" Professor: John Burke | Cours

Chunk 5 (source: prof_shuying_sun_mathematics.txt):
> er and reviewing previously learned material at the beginning of each class is extremely helpful. She is very caring, genuine, patient, and thorough with her teaching." Professor: Shuying Sun | Course: MATH3305 | Rating: 4.0/5 | Difficulty: 3.0/5 "Solid professor. Reasonable amount of homework, does

---

## Embedding Model

**Model used:** all-MiniLM-L6-v2 via sentence-transformers. Runs locally with no API key or rate limits. Downloaded once and cached.

**Production tradeoff reflection:** For a real deployment I would weigh four factors. Cost: text-embedding-3-small (OpenAI) offers higher accuracy but charges per token and adds API latency. Multilingual support: multilingual-e5-base would be needed if students write reviews in Spanish or other languages, which is realistic at a Texas university with international students. Context length: all-MiniLM-L6-v2 has a 256 token limit which fits short reviews well but would truncate long documents. Latency: local models avoid network round trips but require more RAM. For this project, local wins on every dimension that matters.

---

## Retrieval Results

Three sample queries run against the live ChromaDB collection. Distance scores are cosine distances — lower means more semantically similar.

**Query 1: "What do students say about Ted Lehr's teaching style?"**

| Rank | Distance | Source |
|------|----------|--------|
| 1 | 0.5375 | prof_ted_lehr_computer_science.txt |
| 2 | 0.6145 | prof_ted_lehr_computer_science.txt |
| 3 | 0.6478 | prof_ted_lehr_computer_science.txt |
| 4 | 0.7608 | prof_ted_lehr_computer_science.txt |

All 4 results returned from the correct file. Distances are above 0.5 because the reviews discuss classroom behavior and grading style rather than explicitly naming "teaching style," creating a small semantic gap. Retrieval is topically correct despite elevated scores.

**Query 2: "Which math professor is easiest at Texas State?"**

| Rank | Distance | Source |
|------|----------|--------|
| 1 | 0.7648 | prof_ellen_couvillion_mathematics.txt |
| 2 | 0.8663 | prof_jackson_rebrovich_mathematics.txt |
| 3 | 0.8979 | prof_jackson_rebrovich_mathematics.txt |
| 4 | 0.9255 | prof_shuying_sun_mathematics.txt |

All results from math professor files. Distances are higher because "easiest" is an indirect concept not used verbatim in reviews — students use "easy to understand," "understandable," and "manageable" instead. Top result from Couvillion is relevant; her reviews directly address students who are nervous about math.

**Query 3: "What is Professor Zong like for CS courses?"**

| Rank | Distance | Source |
|------|----------|--------|
| 1 | 0.4220 | prof_ziliang_zong_computer_science.txt |
| 2 | 0.4785 | prof_ziliang_zong_computer_science.txt |
| 3 | 0.7473 | prof_ziliang_zong_computer_science.txt |
| 4 | 0.7625 | prof_ziliang_zong_computer_science.txt |

Top two results score below 0.5, indicating strong semantic match. All results from the correct file. Direct name queries consistently produce the lowest distances because the professor's name appears verbatim in every chunk.

---

## Grounded Generation

**System prompt grounding instruction:** "Answer using only the review text provided below. If the answer is not contained in the provided reviews, say so explicitly. Do not draw on outside knowledge about professors or courses."

**How source attribution is surfaced in the response:** Retrieved chunks are passed to the model as numbered context blocks each labeled with their source filename. The sources list in the response is built programmatically from the metadata of retrieved chunks, not left to the model to generate. Every response includes a Sources field listing the filenames used.

---

## Query Interface

The system runs as a Gradio web app on `localhost:7860`. The interface has a single text input labeled "Your question," an Ask button, an Answer output box (8 lines), and a Sources output box (4 lines). Both pressing Enter in the input and clicking Ask trigger the same `handle_query` function, which calls `generate()` and formats the sources list as bullet points.

**Sample interaction transcript:**

> **Question:** What do students say about Ted Lehr?
>
> **Answer:** According to the reviews, students say that Ted Lehr constantly disrespects students and tells everyone to just use AI for everything. He grades based on how much he likes a student, has extremely boring lectures, and calls on students he thinks won't be able to answer. Students describe his communication style as harsh and discouraging, and note that he uses a mocking tone during class discussions. He is very strict about his own rules and has told students that failure to follow them will result in a failing grade.
>
> **Sources:**
> • prof_ted_lehr_computer_science.txt

---

## Example Responses

**Example 1 — In-scope question with clear answer:**

> **Question:** Which math professor would you recommend for someone bad at math?
>
> **Answer:** Based on the reviews, Professor Ellen Couvillion is recommended for students who struggle with math. One review states: "I am bad at math but she made it easy. Her explaining of math is very understandable and clear." She is also described as a great math professor for students nervous about algebra, with lectures that are easy to follow, test reviews closely matching actual tests, and very helpful office hours.
>
> **Sources:**
> • prof_ellen_couvillion_mathematics.txt
> • prof_jackson_rebrovich_mathematics.txt

**Example 2 — Out-of-scope question, explicit refusal:**

> **Question:** What is the best restaurant in San Marcos?
>
> **Answer:** The answer is not contained in the provided reviews. The reviews mention Starbucks, but only as a place where Professor Shuying Sun treated her students, not as a recommendation for the best restaurant in San Marcos.
>
> **Sources:**
> • prof_jackson_rebrovich_mathematics.txt
> • prof_marla_burns_exercise_sport_health_ed.txt
> • prof_shuying_sun_mathematics.txt

The system refused to answer from general knowledge and explicitly stated the information was not in the reviews. The Starbucks mention is a correct observation from the retrieved chunks, not an invented fact.

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about Ted Lehr's teaching style? | Harsh, disrespects students, grades on favoritism | Harsh, discouraging tone, mocking in discussions, grades based on favoritism, boring lectures, strict rules with failing-grade threats | Relevant | Accurate |
| 2 | Which math professor is best for students who struggle with math? | Ellen Couvillion | Ellen Couvillion recommended; described as great math professor who explains algebra clearly, provides similar test reviews, helpful in office hours | Relevant | Accurate |
| 3 | Is Edwin Vargas recommended for CS 1308? | No, not actually intro level | Not recommended; all reviews rate 1.0/5, cite disorganization, complex assignments, lack of grading transparency | Relevant | Accurate |
| 4 | What do students say about Ziliang Zong? | Specific details from his reviews | Mixed: praised for wanting students to succeed and checking in, criticized for being hard to understand and quoting "I care about my paycheck" | Relevant | Accurate |
| 5 | Which professor has the best reviews overall at Texas State? | Ellen Couvillion or Marla Burns | Named Jackson Rebrovich and Ellen Couvillion as tied at 5.0/5; did not surface Marla Burns despite her 5.0 ratings | Partially relevant | Partially accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed:** Which professor has the best reviews overall at Texas State?

**What the system returned:** Ellen Couvillion and Jackson Rebrovich named as tied at 5.0/5, with Shuying Sun mentioned as "one of the best." Marla Burns, who also has 5.0/5 ratings, was not surfaced.

**Root cause (tied to a specific pipeline stage):** Retrieval stage. The query "best reviews overall" semantically matched math professor review language more strongly than other files. With top-k=4, only 4 chunks are returned, all from 1-2 files. The retrieval step cannot surface all 10 professors simultaneously for a comparative query. This is a fundamental limitation of single-query top-k retrieval for cross-document comparison questions.

**What you would change to fix it:** Implement a multi-query strategy that runs one retrieval per professor and aggregates results, or add metadata filtering so users can browse by professor name before asking comparison questions.

---

## Spec Reflection

**One way the spec helped you during implementation:** Writing the chunking strategy in planning.md before touching code forced a concrete decision on chunk size and overlap upfront. This meant the ingest.py implementation matched the design exactly and produced the expected chunk count of 72 on the first run without needing to debug or retune.

**One way your implementation diverged from the spec, and why:** The spec anticipated professor nickname retrieval failures as a key challenge. In practice all test queries used full professor names so this failure mode did not manifest during evaluation. A real deployment with varied student queries would need nickname normalization, but it was not testable with the current evaluation set.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* Document structure (10 .txt files with professor name, course, rating, review text) and chunking strategy section from planning.md specifying 300 character chunks with 50 character overlap.
- *What it produced:* Full implementation of ingest.py with a sliding window chunker and metadata attachment.
- *What I changed or overrode:* Added a minimum chunk length filter (len > 50) to remove fragments that the AI implementation did not include. Verified by printing 5 sample chunks and checking none were incomplete sentences.

**Instance 2**

- *What I gave the AI:* Exact grounding system prompt text and required output format specifying the generate() function must return a dict with answer and sources keys.
- *What it produced:* Full generator.py with Groq API integration and context formatting.
- *What I changed or overrode:* Verified the grounding instruction was included exactly as written and not rephrased. Tested off-topic refusal with a restaurant query to confirm the model refused rather than answering from general knowledge.
