import sqlite3
import subprocess
from pathlib import Path

DB = Path("outputs/spending.db")
MODEL = "llama3.2:3b"

SCHEMA = """
Table: spending

Columns:
- id INTEGER
- date TEXT
- location TEXT
- category TEXT
- description TEXT
- amount REAL
- currency TEXT
- raw_text TEXT
"""


def normalise_question(question):
    return question.lower().strip().rstrip("?!.").strip()


def clean_sql(sql):
    sql = sql.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()
    sql = " ".join(sql.split())
    return sql


def get_known_query(question):
    known_queries = {
        "daily burn excluding big purchases": """
            SELECT SUM(amount) / COUNT(DISTINCT date)
            FROM spending
            WHERE amount < 50000
        """,
        "daily burn excluding large purchases": """
            SELECT SUM(amount) / COUNT(DISTINCT date)
            FROM spending
            WHERE amount < 50000
        """,
        "what is my daily burn excluding big purchases": """
            SELECT SUM(amount) / COUNT(DISTINCT date)
            FROM spending
            WHERE amount < 50000
        """,
        "what is my daily burn excluding large purchases": """
            SELECT SUM(amount) / COUNT(DISTINCT date)
            FROM spending
            WHERE amount < 50000
        """,
        "what is my daily burn": """
            SELECT SUM(amount) / COUNT(DISTINCT date)
            FROM spending
        """,
        "daily burn": """
            SELECT SUM(amount) / COUNT(DISTINCT date)
            FROM spending
        """,
        "how much did i spend": """
            SELECT SUM(amount)
            FROM spending
        """,
        "how much did i spend in japan": """
            SELECT SUM(amount)
            FROM spending
            WHERE LOWER(location) = 'japan'
        """,
        "total spending by category": """
            SELECT category, SUM(amount)
            FROM spending
            GROUP BY category
            ORDER BY SUM(amount) DESC
        """,
        "what is my total spending by category": """
            SELECT category, SUM(amount)
            FROM spending
            GROUP BY category
            ORDER BY SUM(amount) DESC
        """,
    }

    return known_queries.get(question)


def generate_sql_with_llm(question):
    prompt = f"""
You are a SQL generator.

Convert the user's question into a SQLite SELECT query.

Rules:
- Return ONLY SQL.
- No markdown.
- No explanation.
- Only use the spending table.
- Only generate SELECT queries.
- Do not modify the database.
- Use amount for spending calculations.
- Use raw_text and description when searching for specific purchases.
- If asked to exclude large one-off purchases, use amount < 50000.

Important definitions:
- "daily burn" means total spending divided by number of distinct dates.
- "excluding large purchases" means amount < 50000.
- Locations should be matched case-insensitively using LOWER(location).
- If the user asks about Japan, use LOWER(location) = 'japan'.
- Dates are stored as text like "11/05", not full SQL dates.

Schema:
{SCHEMA}

User question:
{question}
"""

    result = subprocess.run(
        ["ollama", "run", MODEL, prompt],
        capture_output=True,
        text=True
    )

    return clean_sql(result.stdout)


def run_sql(sql):
    if not sql.lower().startswith("select"):
        raise ValueError(f"Unsafe/non-SELECT SQL generated:\n{sql}")

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute(sql)
    rows = cursor.fetchall()

    conn.close()
    return rows


def main():
    question = input("Ask a spending question: ")
    normalised = normalise_question(question)

    known_sql = get_known_query(normalised)

    if known_sql:
        sql = clean_sql(known_sql)
    else:
        sql = generate_sql_with_llm(question)

    print("\nGenerated SQL:")
    print(sql)

    rows = run_sql(sql)

    print("\nResult:")
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()