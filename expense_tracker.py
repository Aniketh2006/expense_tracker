"""
Expense Tracker
================
A small command-line application to record personal expenses, view them by
category, and generate a spending summary. Data is persisted to a local
JSON file so it survives between runs.

Author: Aniketh
"""

import json
import os
from datetime import datetime
from typing import Optional

DATA_FILE = "expenses.json"


class ExpenseError(Exception):
    """Raised when an expense entry fails validation."""
    pass


class ExpenseTracker:
    """Manages a collection of expenses: adding, viewing, summarizing, and
    persisting them to disk."""

    def __init__(self, data_file: str = DATA_FILE):
        self.data_file = data_file
        self.expenses = self._load_from_file()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------
    def _load_from_file(self) -> list:
        """Load expenses from the JSON file. Starts fresh if the file
        doesn't exist yet or is corrupted, instead of crashing."""
        if not os.path.exists(self.data_file):
            return []
        try:
            with open(self.data_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            print(f"Warning: could not read '{self.data_file}'. Starting with an empty list.")
            return []

    def save_to_file(self) -> None:
        """Write the current expenses list to disk."""
        with open(self.data_file, "w") as f:
            json.dump(self.expenses, f, indent=2)

    # ------------------------------------------------------------------
    # Core features
    # ------------------------------------------------------------------
    def add_expense(self, amount: float, category: str, description: str = "",
                     date: Optional[str] = None) -> dict:
        """Add a new expense after validating the input.

        Raises:
            ExpenseError: if amount is not a positive number, or category is empty.
        """
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            raise ExpenseError(f"Amount must be a number, got: {amount!r}")

        if amount <= 0:
            raise ExpenseError("Amount must be greater than zero.")

        category = (category or "").strip()
        if not category:
            raise ExpenseError("Category cannot be empty.")

        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        else:
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                raise ExpenseError(f"Date must be in YYYY-MM-DD format, got: {date!r}")

        entry = {
            "amount": round(amount, 2),
            "category": category,
            "description": description.strip(),
            "date": date,
        }
        self.expenses.append(entry)
        return entry

    def view_expenses(self, category: Optional[str] = None) -> list:
        """Return all expenses, or only those matching a category
        (case-insensitive) if one is given."""
        if category is None:
            return list(self.expenses)
        category = category.strip().lower()
        return [e for e in self.expenses if e["category"].lower() == category]

    def get_summary(self) -> dict:
        """Return total spend per category and the overall total.
        Returns an empty summary (no division-by-zero) if there are no expenses.
        """
        summary = {}
        for e in self.expenses:
            summary[e["category"]] = summary.get(e["category"], 0) + e["amount"]

        total = sum(summary.values())
        average = round(total / len(self.expenses), 2) if self.expenses else 0.0

        return {
            "by_category": {k: round(v, 2) for k, v in summary.items()},
            "total": round(total, 2),
            "average_per_expense": average,
            "count": len(self.expenses),
        }

    def delete_expense(self, index: int) -> dict:
        """Delete an expense by its position in the list (0-based).

        Raises:
            ExpenseError: if the index is out of range.
        """
        if index < 0 or index >= len(self.expenses):
            raise ExpenseError(f"No expense at index {index}. There are {len(self.expenses)} expense(s).")
        return self.expenses.pop(index)


# ----------------------------------------------------------------------
# Simple command-line interface
# ----------------------------------------------------------------------
def run_cli():
    tracker = ExpenseTracker()
    menu = """
--- Expense Tracker ---
1. Add expense
2. View all expenses
3. View expenses by category
4. Show summary
5. Delete an expense
6. Save & Exit
"""
    while True:
        print(menu)
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            amount = input("Amount: ").strip()
            category = input("Category: ").strip()
            description = input("Description (optional): ").strip()
            try:
                entry = tracker.add_expense(amount, category, description)
                print(f"Added: {entry}")
            except ExpenseError as e:
                print(f"Could not add expense: {e}")

        elif choice == "2":
            for i, e in enumerate(tracker.view_expenses()):
                print(f"[{i}] {e['date']} | {e['category']} | ₹{e['amount']} | {e['description']}")

        elif choice == "3":
            category = input("Category to filter by: ").strip()
            for i, e in enumerate(tracker.view_expenses(category)):
                print(f"[{i}] {e['date']} | {e['category']} | ₹{e['amount']} | {e['description']}")

        elif choice == "4":
            summary = tracker.get_summary()
            print(f"\nTotal spent: ₹{summary['total']} across {summary['count']} expense(s)")
            print(f"Average per expense: ₹{summary['average_per_expense']}")
            for cat, amt in summary["by_category"].items():
                print(f"  {cat}: ₹{amt}")

        elif choice == "5":
            try:
                index = int(input("Index of expense to delete: ").strip())
                removed = tracker.delete_expense(index)
                print(f"Removed: {removed}")
            except ValueError:
                print("Please enter a valid number.")
            except ExpenseError as e:
                print(f"Could not delete expense: {e}")

        elif choice == "6":
            tracker.save_to_file()
            print("Saved. Goodbye!")
            break

        else:
            print("Invalid option, please choose 1-6.")


if __name__ == "__main__":
    run_cli()
