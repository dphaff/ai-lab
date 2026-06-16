import json
import csv
from pathlib import Path

INPUT = Path("outputs/travel_note.json")
OUTPUT = Path("outputs/spending.csv")

data = json.loads(INPUT.read_text())

rows = []

for day in data:
    for entry in day["entries"]:
        rows.append({
            "date": day["date"],
            "location": day["location"],
            "category": entry["category"],
            "description": entry.get("description", ""),            "amount": entry["amount"],
            "currency": entry["currency"],
            "raw_text": entry["raw_text"]
        })

with OUTPUT.open("w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "date",
            "location",
            "category",
            "description",
            "amount",
            "currency",
            "raw_text"
        ]
    )

    writer.writeheader()
    writer.writerows(rows)

print(f"Exported {len(rows)} rows to {OUTPUT}")