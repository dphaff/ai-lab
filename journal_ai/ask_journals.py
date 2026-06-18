import json
import math
import sqlite3
import subprocess
from pathlib import Path

DB = Path("journal_ai/journal_index.db")

EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "llama3.2:3b"


def get_embedding(text):
    result = subprocess.run(
        ["ollama", "run", EMBED_MODEL, text],
        capture_output=True,
        text=True
    )

    return json.loads(result.stdout)


def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))

    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(x * x for x in b))

    return dot / (mag_a * mag_b)


def get_chunks():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT section_title, section_type, text, embedding
    FROM journal_chunks
    """)

    rows = cursor.fetchall()
    conn.close()

    chunks = []

    for title, section_type, text, embedding in rows:
        chunks.append({
            "title": title,
            "type": section_type,
            "text": text,
            "embedding": json.loads(embedding)
        })

    return chunks


def ask_llm(question, chunks):
    context = "\n\n---\n\n".join(
        [
            f"""
DATE/SECTION:
{chunk['title']}

TYPE:
{chunk['type']}

TEXT:
{chunk['text']}
"""
            for chunk in chunks
        ]
    )

    prompt = f"""
You are analysing my personal journal.

Rules:
- Use only the journal excerpts provided.
- Separate facts from interpretation.
- Mention dates when useful.
- Look for patterns, not motivational advice.

Answer format:
1. Direct answer
2. Evidence by date/section
3. Uncertainties / missing context

Rules:
- Cite the DATE/SECTION for each claim.
- Include frictions/negatives as well as positives.
- If the evidence is mixed, say so.
- Do not give advice unless asked.
- Do not ask follow-up questions.

Journal excerpts:

{context}


Question:
{question}
"""

    result = subprocess.run(
        ["ollama", "run", CHAT_MODEL, prompt],
        capture_output=True,
        text=True
    )

    return result.stdout


def main():
    question = input("Ask your journals: ")

    question_embedding = get_embedding(question)

    chunks = get_chunks()

    scored = []

    for chunk in chunks:
        score = cosine_similarity(
            question_embedding,
            chunk["embedding"]
        )

        scored.append((score, chunk))

    scored.sort(reverse=True, key=lambda x: x[0])

    best_chunks = [
        chunk for score, chunk in scored[:5]
    ]

    print("\nRetrieved:")

    for chunk in best_chunks:
        preview = chunk["text"][:250].replace("\n", " ")
        print(f"- {chunk['title']} ({chunk['type']})")
        print(f"  {preview}...")

    answer = ask_llm(question, best_chunks)

    print("\nAnswer:")
    print(answer)


if __name__ == "__main__":
    main()