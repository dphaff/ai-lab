import json
from pathlib import Path
from parse_note import parse_chunk

PARSED = Path("outputs/travel_note.json")
FAILED = Path("outputs/failed_chunks.txt")

parsed_days = json.loads(PARSED.read_text())
failed_chunks = json.loads(FAILED.read_text())

still_failed = []

for failed in failed_chunks:
    chunk = {
        "date": failed["date"],
        "text": failed["text"]
    }

    print(f"Retrying {chunk['date']}...")

    try:
        data = parse_chunk(chunk)
        parsed_days.append(data)
    except Exception as e:
        still_failed.append({
            "date": chunk["date"],
            "error": str(e),
            "text": chunk["text"]
        })

PARSED.write_text(json.dumps(parsed_days, indent=2, ensure_ascii=False))
FAILED.write_text(json.dumps(still_failed, indent=2, ensure_ascii=False))

print(f"Recovered {len(failed_chunks) - len(still_failed)} chunks")
print(f"Still failed: {len(still_failed)}")