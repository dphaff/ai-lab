import subprocess

MENU = """
Spending AI

1. Import existing JSON into master DB
2. Run category cleanup
3. Review transactions
4. Show analytics summary
5. Ask spending question
6. Exit

Choose an option: """


def run(command):
    subprocess.run(command, shell=True)


def main():
    while True:
        choice = input(MENU).strip()

        if choice == "1":
            run("python3 spending_ai/database/import_from_existing_json.py")

        elif choice == "2":
            run("python3 spending_ai/database/cleanup_categories.py")

        elif choice == "3":
            run("python3 spending_ai/review_transactions.py")

        elif choice == "4":
            run("python3 spending_ai/analytics/summary.py")

        elif choice == "5":
            run("python3 spending_ai/ask_spending.py")

        elif choice == "6":
            print("Exiting.")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()