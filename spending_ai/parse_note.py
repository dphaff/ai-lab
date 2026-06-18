import json
import re
import subprocess
from pathlib import Path

INPUT = Path("inputs/travel_note.txt")
OUTPUT = Path("outputs/travel_note.json")
FAILED = Path("outputs/failed_chunks.txt")

MODEL = "llama3.2:3b"
DEFAULT_LOCATION = "Japan"
DEFAULT_CURRENCY = "JPY"


def split_into_date_chunks(text):
    """
    Splits a messy note into chunks starting with dates like:
    11/05
    1/06
    01/06
    """
    pattern = r"(?m)^\s*(\d{1,2}/\d{1,2})\s*$"
    matches = list(re.finditer(pattern, text))

    chunks = []

    for i, match in enumerate(matches):
        date = match.group(1)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()

        if body:
            chunks.append({
                "date": date,
                "text": body
            })

    return chunks


def extract_json(text):
    """
    Pulls the first JSON object out of messy model output.
    Handles cases where the model adds:
    'Here is the JSON:'
    ```json
    {...}
    ```
    """
    text = text.replace("```json", "").replace("```", "").strip()

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON object found")

    return text[start:end + 1]


def parse_chunk(chunk):
    prompt = f"""
You are extracting travel spending data.

Return ONLY valid JSON.
No markdown.
No explanation.
No comments.

Rules:
- Use this exact date: {chunk["date"]}
- Use this location: {DEFAULT_LOCATION}
- Use this currency: {DEFAULT_CURRENCY}
- amount must be a number, never an expression.
- If the line says "146+306 transport", amount should be 452.
- If the line says "199*2 train", amount should be 398.
- Do not invent entries.
- If unsure about category, use "other".

Allowed categories:
food, accommodation, transport, coffee, shopping, health, entertainment, other

Return this exact shape:

{{
  "date": "{chunk["date"]}",
  "location": "{DEFAULT_LOCATION}",
  "entries": [
    {{
      "raw_text": "original line",
      "category": "food",
      "amount": 123,
      "currency": "{DEFAULT_CURRENCY}",
      "description": "short description"
    }}
  ]
}}

Messy spending lines:

{chunk["text"]}
"""

    result = subprocess.run(
        ["ollama", "run", MODEL, prompt],
        capture_output=True,
        text=True
    )

    raw = result.stdout.strip()
    cleaned = extract_json(raw)
    data = json.loads(cleaned)

    return data


def main():
    text = INPUT.read_text()
    chunks = split_into_date_chunks(text)

    print(f"Found {len(chunks)} date chunks")

    all_days = []
    failed = []

    for chunk in chunks:
        print(f"Parsing {chunk['date']}...")

        try:
            data = parse_chunk(chunk)
            all_days.append(data)
        except Exception as e:
            print(f"First attempt failed for {chunk['date']}, retrying...")

            try:
                data = parse_chunk(chunk)
                all_days.append(data)
            except Exception as e:
                failed.append({
                    })

    OUTPUT.write_text(json.dumps(all_days, indent=2, ensure_ascii=False))

    if failed:
        FAILED.write_text(json.dumps(failed, indent=2, ensure_ascii=False))
        print(f"{len(failed)} chunks failed. See {FAILED}")

    print(f"Saved {len(all_days)} parsed days to {OUTPUT}")


if __name__ == "__main__":
    main()