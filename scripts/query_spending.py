import sqlite3
from pathlib import Path

DB = Path("outputs/spending.db")

conn = sqlite3.connect(DB)
cursor = conn.cursor()

print("\nCATEGORY TOTALS")
cursor.execute("""
SELECT category, SUM(amount) AS total
FROM spending
GROUP BY category
ORDER BY total DESC
""")

for category, total in cursor.fetchall():
    print(f"{category}: ¥{total:,.0f}")

print("\nTOTAL EXCLUDING IPHONE / LARGE PURCHASES")
cursor.execute("""
SELECT SUM(amount)
FROM spending
WHERE amount < 50000
""")

total_ex_big = cursor.fetchone()[0]
print(f"¥{total_ex_big:,.0f}")

print("\nAVERAGE DAILY BURN")
cursor.execute("""
SELECT AVG(daily_total)
FROM (
    SELECT date, SUM(amount) AS daily_total
    FROM spending
    WHERE amount < 50000
    GROUP BY date
)
""")

avg_daily = cursor.fetchone()[0]
print(f"¥{avg_daily:,.0f}")

conn.close()