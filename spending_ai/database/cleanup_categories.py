import sqlite3
from pathlib import Path

DB = Path("spending_ai/spending_master.db")

RULES = [
    ("train", "transport"),
    ("library", "transport"),
    ("baseball", "entertainment"),
    ("cinema", "entertainment"),
    ("umeshu", "entertainment"),
    ("pharmacy", "health"),
    ("deodorant", "health"),
    ("water", "food"),
    ("iphone", "electronics"),
    ("tower", "entertainment"),
]

conn = sqlite3.connect(DB)
cursor = conn.cursor()

for keyword, category in RULES:
    cursor.execute("""
    UPDATE transactions
    SET category = ?
    WHERE LOWER(raw_text) LIKE ?
    """, (category, f"%{keyword}%"))

conn.commit()
conn.close()

print("Cleaned categories")