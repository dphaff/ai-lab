import sqlite3
from pathlib import Path

DB = Path("spending_ai/spending_master.db")

conn = sqlite3.connect(DB)
cursor = conn.cursor()

try:
    cursor.execute("""
    ALTER TABLE transactions
    ADD COLUMN review_status TEXT DEFAULT 'unreviewed'
    """)

    print("Added review_status column")

except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("review_status already exists")
    else:
        raise

conn.commit()
conn.close()