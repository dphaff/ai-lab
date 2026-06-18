from pathlib import Path
from build_index import split_into_chunks

FILE = Path("journal_ai/journals/may_2026.md")

text = FILE.read_text()
chunks = split_into_chunks(text, FILE.name)

print(f"Found {len(chunks)} chunks\n")

for i, chunk in enumerate(chunks[:15], start=1):    
    preview = chunk["text"][:300].replace("\n", " ")

    print("=" * 80)
    print(f"Chunk {i}")
    print(f"Title: {chunk['section_title']}")
    print(f"Type: {chunk.get('section_type', 'unknown')}")
    print(f"Length: {len(chunk['text'])} characters")
    print(f"Preview: {preview}")