# Expense Tracker

A small command-line Python application for recording personal expenses,
viewing them by category, and generating a spending summary. Data is saved
to a local JSON file so it persists between runs.

Built as part of Week 5 of the Gen AI Internship at Davine Technologies —
developed with AI assistance for code generation, debugging, documentation,
and test writing, then reviewed and verified manually.

## Features

- Add an expense with amount, category, description, and date
- View all expenses, or filter by category
- Get a summary: total spend, average per expense, and totals by category
- Delete an expense by index
- Input validation (rejects negative/zero amounts, empty categories, bad date formats)
- Data persisted to `expenses.json` between sessions

## Requirements

- Python 3.8 or higher (no external packages needed — standard library only)

## Usage

Run the interactive CLI:

```bash
python3 expense_tracker.py
```

You'll see a menu:

```
--- Expense Tracker ---
1. Add expense
2. View all expenses
3. View expenses by category
4. Show summary
5. Delete an expense
6. Save & Exit
```

### Using it as a library

```python
from expense_tracker import ExpenseTracker, ExpenseError

tracker = ExpenseTracker()
tracker.add_expense(500, "Food", "Groceries", "2026-08-31")

try:
    tracker.add_expense(-100, "Food")
except ExpenseError as e:
    print(e)  # "Amount must be greater than zero."

summary = tracker.get_summary()
print(summary)
# {'by_category': {'Food': 500.0}, 'total': 500.0, 'average_per_expense': 500.0, 'count': 1}

tracker.save_to_file()
```

## Running Tests

```bash
python3 -m unittest test_expense_tracker.py -v
```

All 12 tests should pass. They cover valid input, rejected invalid input
(negative amounts, empty categories, bad dates), category filtering,
summary calculation (including the empty-list edge case), deleting
expenses, and save/reload persistence.

## Project Structure

```
expense_tracker/
├── expense_tracker.py       # main application (ExpenseTracker class + CLI)
├── test_expense_tracker.py  # unit tests
└── README.md
```

## Known Limitations

- Single-user, single-file storage — not built for concurrent access.
- No currency conversion; amounts are assumed to be in one currency.
- CLI only — no GUI or web interface.
