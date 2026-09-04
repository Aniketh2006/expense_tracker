"""
Unit tests for expense_tracker.py
Run with: python -m unittest test_expense_tracker.py -v
"""

import unittest
import os
from expense_tracker import ExpenseTracker, ExpenseError


class TestExpenseTracker(unittest.TestCase):

    def setUp(self):
        # use a throwaway test file so we never touch real data
        self.test_file = "test_expenses_temp.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.tracker = ExpenseTracker(data_file=self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_valid_expense(self):
        entry = self.tracker.add_expense(250, "Food", "Lunch", "2026-08-31")
        self.assertEqual(entry["amount"], 250.0)
        self.assertEqual(entry["category"], "Food")
        self.assertEqual(len(self.tracker.expenses), 1)

    def test_add_expense_rejects_negative_amount(self):
        with self.assertRaises(ExpenseError):
            self.tracker.add_expense(-100, "Food")

    def test_add_expense_rejects_zero_amount(self):
        with self.assertRaises(ExpenseError):
            self.tracker.add_expense(0, "Food")

    def test_add_expense_rejects_non_numeric_amount(self):
        with self.assertRaises(ExpenseError):
            self.tracker.add_expense("abc", "Food")

    def test_add_expense_rejects_empty_category(self):
        with self.assertRaises(ExpenseError):
            self.tracker.add_expense(100, "   ")

    def test_add_expense_rejects_bad_date_format(self):
        with self.assertRaises(ExpenseError):
            self.tracker.add_expense(100, "Food", date="31-08-2026")

    def test_view_expenses_filters_by_category_case_insensitive(self):
        self.tracker.add_expense(100, "Food")
        self.tracker.add_expense(200, "food")
        self.tracker.add_expense(300, "Travel")
        food_expenses = self.tracker.view_expenses("FOOD")
        self.assertEqual(len(food_expenses), 2)

    def test_summary_with_no_expenses_does_not_crash(self):
        summary = self.tracker.get_summary()
        self.assertEqual(summary["total"], 0.0)
        self.assertEqual(summary["average_per_expense"], 0.0)
        self.assertEqual(summary["count"], 0)

    def test_summary_calculates_totals_correctly(self):
        self.tracker.add_expense(100, "Food")
        self.tracker.add_expense(200, "Food")
        self.tracker.add_expense(50, "Travel")
        summary = self.tracker.get_summary()
        self.assertEqual(summary["total"], 350.0)
        self.assertEqual(summary["by_category"]["Food"], 300.0)
        self.assertEqual(summary["count"], 3)

    def test_delete_expense_removes_correct_entry(self):
        self.tracker.add_expense(100, "Food")
        self.tracker.add_expense(200, "Travel")
        removed = self.tracker.delete_expense(0)
        self.assertEqual(removed["category"], "Food")
        self.assertEqual(len(self.tracker.expenses), 1)

    def test_delete_expense_invalid_index_raises_error(self):
        with self.assertRaises(ExpenseError):
            self.tracker.delete_expense(5)

    def test_save_and_reload_persists_data(self):
        self.tracker.add_expense(100, "Food")
        self.tracker.save_to_file()
        reloaded = ExpenseTracker(data_file=self.test_file)
        self.assertEqual(len(reloaded.expenses), 1)
        self.assertEqual(reloaded.expenses[0]["category"], "Food")


if __name__ == "__main__":
    unittest.main()
