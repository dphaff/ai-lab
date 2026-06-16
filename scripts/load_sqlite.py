import json
import sqlite3
from pathlib import Path

INPUT = Path("outputs/travel_note.json")
DB = Path("outputs/spending.db")

data = json.loads(INPUT.read_text())

conn = sqlite3.connect(DB)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS spending (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    location TEXT,
    category TEXT,
    description TEXT,
    amount REAL,
    currency TEXT,
    raw_text TEXT
)
""")

cursor.execute("DELETE FROM spending")

for day in data:
    for entry in day.get("entries", []):
        cursor.execute("""
        INSERT INTO spending (
            date, location, category, description, amount, currency, raw_text
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            day.get("date", ""),
            day.get("location", ""),
            entry.get("category", "other"),
            entry.get("description", ""),
            entry.get("amount", None),
            entry.get("currency", "JPY"),
            entry.get("raw_text", "")
        ))

conn.commit()
conn.close()

print(f"Loaded spending data into {DB}")