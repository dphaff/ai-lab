import sqlite3
from pathlib import Path

DB = Path("spending_ai/spending_master.db")

VALID_CATEGORIES = [
    "food",
    "coffee",
    "transport",
    "accommodation",
    "shopping",
    "health",
    "entertainment",
    "electronics",
    "other",
]


def yen(value):
    if value is None:
        return "¥0 / missing amount"
    return f"¥{value:,.0f}"


conn = sqlite3.connect(DB)
cursor = conn.cursor()

cursor.execute("""
SELECT id, date, amount, category, raw_text, review_status
FROM transactions
WHERE review_status = 'unreviewed'
AND (category = 'other' OR amount >= 5000)
ORDER BY amount DESC
""")

rows = cursor.fetchall()

print(f"Found {len(rows)} transactions to review")

for row in rows:
    tx_id, date, amount, category, raw_text, review_status = row

    print("\n" + "=" * 70)
    print(f"ID: {tx_id}")
    print(f"Date: {date}")
    print(f"Amount: {yen(amount)}")
    print(f"Current category: {category}")
    print(f"Raw text: {raw_text}")

    print("\nOptions:")
    print("Enter = approve")
    print("s = skip")
    print("q = quit")
    print("or type new category")

    choice = input("> ").strip().lower()

    if choice == "q":
        break

    if choice == "s":
        continue

    if choice == "":
        cursor.execute("""
        UPDATE transactions
        SET review_status = 'manual_reviewed'
        WHERE id = ?
        """, (tx_id,))
        conn.commit()
        print("Approved")
        continue

    if choice not in VALID_CATEGORIES:
        print(f"Invalid category: {choice}")
        print(f"Valid categories: {', '.join(VALID_CATEGORIES)}")
        continue

    cursor.execute("""
    UPDATE transactions
    SET category = ?, review_status = 'manual_reviewed'
    WHERE id = ?
    """, (choice, tx_id))

    conn.commit()
    print(f"Updated category to {choice}")

conn.close()
print("\nReview complete")