'''Problem: Student Task Manager
Build a Python program that manages a list of tasks.
Each task has:
title
status
Example:
"Complete assignment" → "pending"
"Practice coding" → "completed"
Your program should allow the user to:
1. Add a task
Example:Enter task: Complete assignment
Store it as a pending task.
2. View all tasks
Display something like:
1. Complete assignment - pending
2. Practice coding - completed
3. Mark a task as completed
The user chooses the task number.
4. Exit
The program should stop.
Requirements
Your program should have a menu:
1. Add Task
2. View Tasks
3. Complete Task
4. Exit
It should continue showing the menu until the user chooses 4.
Also handle:
no tasks available
invalid menu choices
invalid task numbers
'''

tasks = []

while True:
	print("\n1. Add Task")
	print("2. View Tasks")
	print("3. Complete Task")
	print("4. Exit")

	choice = input("Choose an option: ")

	if choice == "1":
		title = input("Enter task: ")
		tasks.append({"title": title, "status": "pending"})
		print("Task added.")
	elif choice == "2":
		if not tasks:
			print("No tasks available.")
		else:
			for number, task in enumerate(tasks, start=1):
				print(f"{number}. {task['title']} - {task['status']}")
	elif choice == "3":
		if not tasks:
			print("No tasks available.")
		else:
			try:
				number = int(input("Enter task number: "))
				if 1 <= number <= len(tasks):
					tasks[number - 1]["status"] = "completed"
					print("Task completed.")
				else:
					print("Invalid task number.")
			except ValueError:
				print("Invalid task number.")
	elif choice == "4":
		print("Goodbye!")
		break
	else:
		print("Invalid menu choice.")