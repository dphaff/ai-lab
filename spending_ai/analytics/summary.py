import sqlite3
from pathlib import Path

DB = Path("spending_ai/spending_master.db")

def yen(value):
    if value is None:
        return "¥0"
    return f"¥{value:,.0f}"

conn = sqlite3.connect(DB)
cursor = conn.cursor()

print("\nTOTAL SPEND")
cursor.execute("SELECT SUM(amount) FROM transactions")
print(yen(cursor.fetchone()[0]))

print("\nDAILY BURN")
cursor.execute("""
SELECT SUM(amount) / COUNT(DISTINCT date)
FROM transactions
""")
print(f"{yen(cursor.fetchone()[0])} / day")

print("\nDAILY BURN EXCLUDING LARGE PURCHASES")
cursor.execute("""
SELECT SUM(amount) / COUNT(DISTINCT date)
FROM transactions
WHERE amount < 50000
""")
print(f"{yen(cursor.fetchone()[0])} / day")

print("\nCATEGORY TOTALS")
cursor.execute("""
SELECT category, SUM(amount)
FROM transactions
GROUP BY category
ORDER BY SUM(amount) DESC
""")
for category, total in cursor.fetchall():
    print(f"{category}: {yen(total)}")

print("\nBIG EXPENSES")
cursor.execute("""
SELECT date, category, amount, description, raw_text
FROM transactions
WHERE amount >= 5000
ORDER BY amount DESC
""")
for date, category, amount, description, raw_text in cursor.fetchall():
    print(f"{date} | {category} | {yen(amount)} | {description or raw_text}")

print("\nUNCATEGORISED / OTHER")
cursor.execute("""
SELECT date, amount, raw_text
FROM transactions
WHERE category = 'other'
ORDER BY amount DESC
""")
for date, amount, raw_text in cursor.fetchall():
    print(f"{date} | {yen(amount)} | {raw_text}")

conn.close()