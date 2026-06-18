import json
import sqlite3
from pathlib import Path

SOURCE = Path("outputs/travel_note.json")
DB = Path("spending_ai/spending_master.db")

conn = sqlite3.connect(DB)
cursor = conn.cursor()

data = json.loads(SOURCE.read_text())

for day in data:
    for entry in day.get("entries", []):
        cursor.execute("""
        INSERT INTO transactions (
            date, amount, currency, country, category, description,
            source, payment_method, shared_status, reimbursement_status,
            confidence, raw_text, notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            day.get("date"),
            entry.get("amount"),
            entry.get("currency", "JPY"),
            "Japan",
            entry.get("category", "other"),
            entry.get("description", ""),
            "travel_note",
            "unknown",
            "unknown",
            "unknown",
            0.7,
            entry.get("raw_text", ""),
            "Imported from original travel_note.json prototype"
        ))

conn.commit()
conn.close()

print("Imported existing Japan note transactions into master database")