import json

FILE_NAME = "leave_management_data.json"


def default_data():
    return {
        "employees": [],
        "leave_requests": [],
        "next_employee_id": 1,
        "next_request_id": 1,
    }


def load_data():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return default_data()

    if not isinstance(data, dict):
        return default_data()

    employees = data.get("employees", [])
    leave_requests = data.get("leave_requests", [])

    if not isinstance(employees, list):
        employees = []
    if not isinstance(leave_requests, list):
        leave_requests = []

    try:
        next_employee_id = int(data.get("next_employee_id", 1))
        next_request_id = int(data.get("next_request_id", 1))
    except (TypeError, ValueError):
        next_employee_id = 1
        next_request_id = 1

    return {
        "employees": employees,
        "leave_requests": leave_requests,
        "next_employee_id": max(next_employee_id, 1),
        "next_request_id": max(next_request_id, 1),
    }


def save_data(data):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def find_employee(data, employee_id):
    for employee in data["employees"]:
        if employee.get("employee_id") == employee_id:
            return employee
    return None


def find_leave_request(data, request_id):
    for request in data["leave_requests"]:
        if request.get("request_id") == request_id:
            return request
    return None


def show_menu():
    print("\nEmployee Leave Management System")
    print("1. Add Employee")
    print("2. View Employees")
    print("3. Apply for Leave")
    print("4. View Leave Requests")
    print("5. Approve/Reject Leave")
    print("6. View Employee Leave Balance")
    print("7. Exit")


def add_employee(data):
    name = input("Enter employee name: ").strip()
    if not name:
        print("Employee name cannot be empty.")
        return

    department = input("Enter department: ").strip()
    if not department:
        print("Department cannot be empty.")
        return

    employee = {
        "employee_id": data["next_employee_id"],
        "name": name,
        "department": department,
        "leave_balance": 20,
    }

    data["employees"].append(employee)
    data["next_employee_id"] += 1
    save_data(data)
    print(f"Employee added successfully. Employee ID: {employee['employee_id']}")


def view_employees(data):
    if not data["employees"]:
        print("No employees available.")
        return

    for employee in data["employees"]:
        print(
            f"ID: {employee['employee_id']}, Name: {employee['name']}, "
            f"Department: {employee['department']}, Leave Balance: {employee['leave_balance']}"
        )


def apply_leave(data):
    if not data["employees"]:
        print("No employees available.")
        return

    try:
        employee_id = int(input("Enter employee ID: ").strip())
    except ValueError:
        print("Invalid employee ID.")
        return

    employee = find_employee(data, employee_id)
    if employee is None:
        print("Invalid employee ID.")
        return

    try:
        days = int(input("Enter number of leave days: ").strip())
    except ValueError:
        print("Leave days must be a valid positive integer.")
        return

    if days <= 0:
        print("Leave days must be greater than zero.")
        return

    reason = input("Enter reason for leave: ").strip()
    if not reason:
        print("Reason cannot be empty.")
        return

    if days > employee["leave_balance"]:
        print("Leave days greater than available balance.")
        return

    request = {
        "request_id": data["next_request_id"],
        "employee_id": employee_id,
        "days": days,
        "reason": reason,
        "status": "Pending",
    }

    data["leave_requests"].append(request)
    data["next_request_id"] += 1
    save_data(data)
    print(f"Leave request submitted successfully. Request ID: {request['request_id']}")


def view_leave_requests(data):
    if not data["leave_requests"]:
        print("No leave requests available.")
        return

    for request in data["leave_requests"]:
        print(
            f"Request ID: {request['request_id']}, Employee ID: {request['employee_id']}, "
            f"Days: {request['days']}, Reason: {request['reason']}, Status: {request['status']}"
        )


def process_leave_request(data):
    if not data["leave_requests"]:
        print("No leave requests available.")
        return

    try:
        request_id = int(input("Enter request ID: ").strip())
    except ValueError:
        print("Invalid leave request ID.")
        return

    request = find_leave_request(data, request_id)
    if request is None:
        print("Invalid leave request ID.")
        return

    if request["status"] in ("Approved", "Rejected"):
        print("This request has already been processed.")
        return

    choice = input("Approve or Reject? Enter 1 for Approve, 2 for Reject: ").strip()

    if choice == "1":
        employee = find_employee(data, request["employee_id"])
        if employee is None:
            print("Employee not found.")
            return

        if request["days"] > employee["leave_balance"]:
            print("Leave days greater than available balance.")
            return

        request["status"] = "Approved"
        employee["leave_balance"] -= request["days"]
        save_data(data)
        print("Leave request approved.")

    elif choice == "2":
        request["status"] = "Rejected"
        save_data(data)
        print("Leave request rejected.")

    else:
        print("Invalid approval/rejection option.")


def view_employee_leave_balance(data):
    if not data["employees"]:
        print("No employees available.")
        return

    try:
        employee_id = int(input("Enter employee ID: ").strip())
    except ValueError:
        print("Invalid employee ID.")
        return

    employee = find_employee(data, employee_id)
    if employee is None:
        print("Invalid employee ID.")
        return

    print(f"Employee: {employee['name']}")
    print(f"Leave Balance: {employee['leave_balance']} days")


def main():
    data = load_data()

    while True:
        show_menu()
        choice = input("Select an option: ").strip()

        if choice == "1":
            add_employee(data)
        elif choice == "2":
            view_employees(data)
        elif choice == "3":
            apply_leave(data)
        elif choice == "4":
            view_leave_requests(data)
        elif choice == "5":
            process_leave_request(data)
        elif choice == "6":
            view_employee_leave_balance(data)
        elif choice == "7":
            print("Exiting system.")
            break
        else:
            print("Invalid menu choice.")


if __name__ == "__main__":
    main()

