import json
from pathlib import Path
from collections import defaultdict

INPUT = Path("outputs/travel_note.json")

data = json.loads(INPUT.read_text())

category_totals = defaultdict(float)
daily_totals = defaultdict(float)

for day in data:
    date = day["date"]

    for entry in day["entries"]:
        amount = entry.get("amount")

        if isinstance(amount, (int, float)):
            category = entry.get("category", "other")
            category_totals[category] += amount
            daily_totals[date] += amount

print("\nCATEGORY TOTALS")
for category, total in sorted(category_totals.items()):
    print(f"{category}: ¥{total:,.0f}")

print("\nDAILY TOTALS")
for date, total in sorted(daily_totals.items()):
    print(f"{date}: ¥{total:,.0f}")

print(f"\nTOTAL: ¥{sum(category_totals.values()):,.0f}")