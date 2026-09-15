import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

import ems


class ExpenseManagementTests(unittest.TestCase):
    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.expenses_file = os.path.join(self.temp_directory.name, "expenses.json")
        self.original_file_name = ems.FILE_NAME
        ems.FILE_NAME = self.expenses_file

    def tearDown(self):
        ems.FILE_NAME = self.original_file_name
        self.temp_directory.cleanup()

    def test_load_missing_file_returns_empty_list(self):
        self.assertEqual(ems.load_expenses(), [])

    def test_load_corrupted_json_returns_empty_list(self):
        with open(self.expenses_file, "w") as file:
            file.write("{invalid json")

        self.assertEqual(ems.load_expenses(), [])

    def test_load_non_list_json_returns_empty_list(self):
        with open(self.expenses_file, "w") as file:
            json.dump({"expense": "invalid format"}, file)

        self.assertEqual(ems.load_expenses(), [])

    def test_save_and_load_expenses(self):
        expenses = [{
            "id": 1,
            "description": "Lunch",
            "category": "Food",
            "amount": 150.0,
        }]

        ems.save_expenses(expenses)

        self.assertEqual(ems.load_expenses(), expenses)

    def test_add_expense_rejects_empty_fields_and_invalid_amounts(self):
        expenses = []
        user_inputs = [
            "", "Lunch",
            "", "Food",
            "not a number", "-10", "150",
        ]

        with patch("builtins.input", side_effect=user_inputs):
            output = StringIO()
            with redirect_stdout(output):
                ems.add_expense(expenses)

        self.assertEqual(expenses[0]["description"], "Lunch")
        self.assertEqual(expenses[0]["category"], "Food")
        self.assertEqual(expenses[0]["amount"], 150.0)
        self.assertIn("Description cannot be empty.", output.getvalue())
        self.assertIn("Category cannot be empty.", output.getvalue())
        self.assertEqual(
            output.getvalue().count("Enter a valid non-negative amount."),
            2,
        )

    def test_add_expense_generates_next_id(self):
        expenses = [{
            "id": 4,
            "description": "Existing",
            "category": "Other",
            "amount": 10.0,
        }]

        with patch("builtins.input", side_effect=["New", "Other", "20"]):
            ems.add_expense(expenses)

        self.assertEqual(expenses[-1]["id"], 5)

    def test_view_empty_expenses(self):
        output = StringIO()
        with redirect_stdout(output):
            ems.view_expenses([])

        self.assertIn("No expenses available.", output.getvalue())

    def test_filter_category_is_case_insensitive(self):
        expenses = [{
            "id": 1,
            "description": "Lunch",
            "category": "Food",
            "amount": 150.0,
        }]

        with patch("builtins.input", return_value="fOoD"):
            output = StringIO()
            with redirect_stdout(output):
                ems.filter_by_category(expenses)

        self.assertIn("Lunch", output.getvalue())

    def test_filter_category_reports_no_match(self):
        with patch("builtins.input", return_value="Travel"):
            output = StringIO()
            with redirect_stdout(output):
                ems.filter_by_category([])

        self.assertIn("No expenses found for this category.", output.getvalue())

    def test_calculate_total_for_expenses(self):
        expenses = [
            {"id": 1, "description": "Lunch", "category": "Food", "amount": 150.0},
            {"id": 2, "description": "Bus", "category": "Travel", "amount": 50.0},
        ]

        output = StringIO()
        with redirect_stdout(output):
            ems.calculate_total(expenses)

        self.assertIn("Total Expense: 200.00", output.getvalue())

    def test_calculate_total_for_empty_list(self):
        output = StringIO()
        with redirect_stdout(output):
            ems.calculate_total([])

        self.assertIn("Total Expense: 0.00", output.getvalue())

    def test_show_highest_expense(self):
        expenses = [
            {"id": 1, "description": "Lunch", "category": "Food", "amount": 150.0},
            {"id": 2, "description": "Rent", "category": "Home", "amount": 900.0},
        ]

        output = StringIO()
        with redirect_stdout(output):
            ems.show_highest_expense(expenses)

        self.assertIn("Rent", output.getvalue())
        self.assertIn("900.00", output.getvalue())

    def test_show_highest_expense_for_empty_list(self):
        output = StringIO()
        with redirect_stdout(output):
            ems.show_highest_expense([])

        self.assertIn("No expenses available.", output.getvalue())

    def test_main_handles_invalid_menu_choice_and_exit(self):
        with patch("builtins.input", side_effect=["9", "6"]):
            output = StringIO()
            with redirect_stdout(output):
                ems.main()

        self.assertIn("Invalid choice.", output.getvalue())
        self.assertIn("Goodbye.", output.getvalue())


if __name__ == "__main__":
    unittest.main()
