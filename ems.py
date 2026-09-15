import json


FILE_NAME = "expenses.json"


def load_expenses():
	try:
		with open(FILE_NAME, "r") as file:
			expenses = json.load(file)
			return expenses if isinstance(expenses, list) else []
	except (FileNotFoundError, json.JSONDecodeError):
		return []


def save_expenses(expenses):
	with open(FILE_NAME, "w") as file:
		json.dump(expenses, file, indent=4)


def display_expense(expense):
	print(f"ID: {expense['id']}")
	print(f"Description: {expense['description']}")
	print(f"Category: {expense['category']}")
	print(f"Amount: {expense['amount']:.2f}")


def add_expense(expenses):
	description = input("Enter description: ").strip()
	while not description:
		print("Description cannot be empty.")
		description = input("Enter description: ").strip()

	category = input("Enter category: ").strip()
	while not category:
		print("Category cannot be empty.")
		category = input("Enter category: ").strip()

	while True:
		amount_text = input("Enter amount: ").strip()
		try:
			amount = float(amount_text)
			if amount < 0:
				raise ValueError
			break
		except ValueError:
			print("Enter a valid non-negative amount.")

	next_id = max((expense["id"] for expense in expenses), default=0) + 1
	expenses.append({
		"id": next_id,
		"description": description,
		"category": category,
		"amount": amount,
	})
	save_expenses(expenses)
	print("Expense added successfully.")


def view_expenses(expenses):
	if not expenses:
		print("No expenses available.")
		return

	for expense in expenses:
		display_expense(expense)
		print("-" * 20)


def filter_by_category(expenses):
	category = input("Enter category: ").strip().lower()
	matches = [
		expense for expense in expenses
		if expense["category"].lower() == category
	]

	if not matches:
		print("No expenses found for this category.")
		return

	for expense in matches:
		display_expense(expense)
		print("-" * 20)


def calculate_total(expenses):
	total = sum(expense["amount"] for expense in expenses)
	print(f"Total Expense: {total:.2f}")


def show_highest_expense(expenses):
	if not expenses:
		print("No expenses available.")
		return

	highest = max(expenses, key=lambda expense: expense["amount"])
	print("Highest Expense:")
	display_expense(highest)


def main():
	expenses = load_expenses()

	while True:
		print("\nExpense Management System")
		print("1. Add Expense")
		print("2. View All Expenses")
		print("3. Filter Expenses by Category")
		print("4. Calculate Total Expense")
		print("5. Show Highest Expense")
		print("6. Exit")

		choice = input("Enter your choice: ").strip()
		if choice == "1":
			add_expense(expenses)
		elif choice == "2":
			view_expenses(expenses)
		elif choice == "3":
			filter_by_category(expenses)
		elif choice == "4":
			calculate_total(expenses)
		elif choice == "5":
			show_highest_expense(expenses)
		elif choice == "6":
			print("Goodbye.")
			break
		else:
			print("Invalid choice. Please select 1 to 6.")


if __name__ == "__main__":
	main()