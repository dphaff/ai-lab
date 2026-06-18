import sqlite3
from pathlib import Path

DB = Path("spending_ai/spending_master.db")

conn = sqlite3.connect(DB)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    amount REAL,
    currency TEXT,
    country TEXT,
    category TEXT,
    description TEXT,
    source TEXT,
    payment_method TEXT,
    shared_status TEXT,
    reimbursement_status TEXT,
    confidence REAL,
    raw_text TEXT,
    notes TEXT
)
""")

conn.commit()
conn.close()

print(f"Created database: {DB}")