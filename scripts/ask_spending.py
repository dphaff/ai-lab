import sqlite3
from pathlib import Path

DB = Path("outputs/spending.db")


def normalise_question(question):
    return question.lower().strip().rstrip("?!.").strip()


def detect_intent(question):
    q = normalise_question(question)

    if "daily burn" in q and any(word in q for word in ["big", "large", "one-off", "expensive"]):
        return "daily_burn_excluding_large"

    if "daily burn" in q:
        return "daily_burn"

    if "category" in q:
        return "category_totals"

    if "food" in q:
        return "food_total"

    if "japan" in q and any(word in q for word in ["spend", "spent", "total"]):
        return "total_japan"

    if any(word in q for word in ["spend", "spent", "total"]):
        return "total"

    return "unknown"


SQL_BY_INTENT = {
    "daily_burn_excluding_large": """
        SELECT SUM(amount) / COUNT(DISTINCT date)
        FROM spending
        WHERE amount < 50000
    """,
    "daily_burn": """
        SELECT SUM(amount) / COUNT(DISTINCT date)
        FROM spending
    """,
    "category_totals": """
        SELECT category, SUM(amount)
        FROM spending
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """,
    "food_total": """
        SELECT SUM(amount)
        FROM spending
        WHERE category = 'food'
    """,
    "total_japan": """
        SELECT SUM(amount)
        FROM spending
        WHERE LOWER(location) = 'japan'
    """,
    "total": """
        SELECT SUM(amount)
        FROM spending
    """,
}


def run_sql(sql):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    return rows


def yen(value):
    if value is None:
        return "¥0"
    return f"¥{value:,.0f}"


def print_answer(intent, rows):
    print("\nAnswer:")

    if intent in ["daily_burn", "daily_burn_excluding_large"]:
        print(f"{yen(rows[0][0])} per day")

    elif intent in ["total", "total_japan", "food_total"]:
        print(yen(rows[0][0]))

    elif intent == "category_totals":
        for category, total in rows:
            print(f"{category}: {yen(total)}")

    else:
        print(rows)


def main():
    question = input("Ask a spending question: ")

    intent = detect_intent(question)

    if intent == "unknown":
        print("\nI don't know how to answer that yet.")
        print("Try: daily burn, total spending, food total, category totals.")
        return

    sql = SQL_BY_INTENT[intent]

    print(f"\nDetected intent: {intent}")
    print("\nSQL:")
    print(" ".join(sql.split()))

    rows = run_sql(sql)
    print_answer(intent, rows)


if __name__ == "__main__":
    main()