import json
import math
import re
import sqlite3
import subprocess
from pathlib import Path

JOURNAL_DIR = Path("journal_rag/journal_files")
DB = Path("journal_rag/journal_index.db")
EMBED_MODEL = "nomic-embed-text"


def split_into_chunks(text, source_file):
    pattern = r"(?m)^(\d{2}/\d{2}/\d{2})"

    matches = list(re.finditer(pattern, text))

    chunks = []

    for i, match in enumerate(matches):
        start = match.start()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)

        section = text[start:end].strip()

        title = match.group(1)

        first_line = section.splitlines()[0].strip()
        title = first_line

        if "Wins:" in section and "Frictions:" in section and "Energy In:" in section:
            section_type = "era_review"
        else:
            section_type = "daily_journal"

        chunks.append({
            "source_file": source_file,
            "section_title": title,
            "section_type": section_type,
            "text": section
        })

    return chunks


def get_embedding(text):
    prompt = text.replace("\n", " ")

    for attempt in range(3):
        result = subprocess.run(
            ["ollama", "run", EMBED_MODEL, prompt],
            capture_output=True,
            text=True
        )

        raw = result.stdout.strip()

        if not raw:
            print(f"Empty embedding response. Retry {attempt + 1}/3")
            continue

        try:
            data = json.loads(raw)

            if isinstance(data, list):
                return data

            if isinstance(data, dict) and "embedding" in data:
                return data["embedding"]

        except Exception:
            print(f"Bad embedding response. Retry {attempt + 1}/3")

    raise ValueError("Embedding failed after 3 retries")

def create_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS journal_chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_file TEXT,
        section_title TEXT,
        section_type TEXT,
        text TEXT,
        embedding TEXT
    )
    """)

    cursor.execute("DELETE FROM journal_chunks")

    conn.commit()
    conn.close()


def save_chunk(chunk, embedding):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO journal_chunks (
        source_file, section_title, section_type, text, embedding
    )
    VALUES (?, ?, ?, ?, ?)
    """, (
        chunk["source_file"],
        chunk["section_title"],
        chunk["section_type"],
        chunk["text"],
        json.dumps(embedding)
    ))

    conn.commit()
    conn.close()


def main():
    create_db()

    files = list(JOURNAL_DIR.glob("*.md"))
    print(f"Found {len(files)} journal files")

    total_chunks = 0

    for file in files:
        text = file.read_text()
        chunks = split_into_chunks(text, file.name)

        print(f"{file.name}: {len(chunks)} chunks")

        for chunk in chunks:
            print(f"Embedding: {chunk['section_title'][:60]}")
            embedding = get_embedding(chunk["text"])
            save_chunk(chunk, embedding)
            total_chunks += 1

    print(f"Saved {total_chunks} chunks to {DB}")


if __name__ == "__main__":
    main()