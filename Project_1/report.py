"""Generating Reports"""

# ----------------------------------
# METHODS
# ___________________________________

def total_employees(employees):
    if not isinstance(employees, dict):
        raise TypeError("Employees must be a dictionary.")
    return len(employees)


def highest_paid_employee(employees):
    if not employees:
        return None
    return max(employees.values(), key=lambda e: e.salary)


def department_salary_expense(departments, employees):
    if not isinstance(departments, dict):
        raise TypeError("Departments must be a dictionary.")
    if not isinstance(employees, dict):
        raise TypeError("Employees must be a dictionary.")

    data = {}
    for dept in departments.values():
        try:
            data[dept.dept_name] = dept.total_salary_expense(employees)
        except Exception:
            data[dept.dept_name] = 0
    return data


def active_projects(projects):
    if not isinstance(projects, dict):
        raise TypeError("Projects must be a dictionary.")


    return {
        p.project_name: len(p.assigned_employee)
        for p in projects.values()
    }


# ----------------------------------------
# CLI FUNCTIONS
# -----------------------------------------

def reporting_cli(employees, departments, projects):
    while True:
        print("""
        -----Reporting Menu-----
        1. Total Employees
        2. Highest Paid Employee
        3. Department-wise Salary Expense
        4. Active Projects
        0. Back to Main Menu
        """)

        try:
            choice = int(input("Choice: "))
        except ValueError:
            print("Invalid input. Enter a number.")
            continue

        if choice == 0:
            break

        elif choice == 1:
            try:
                print("Total Employees:", total_employees(employees))
            except Exception as e:
                print("Error:", e)

        elif choice == 2:
            try:
                emp = highest_paid_employee(employees)
                if emp:
                    print(f"Highest Paid: {emp.name}, Salary: {emp.salary}")
                else:
                    print("No employees available.")
            except Exception as e:
                print("Error:", e)

        elif choice == 3:
            try:
                expenses = department_salary_expense(departments, employees)
                print("\n--- Department Salary Expense ---")
                for dept, total in expenses.items():
                    print(f"{dept}: {total}")
            except Exception as e:
                print("Error:", e)

        elif choice == 4:
            try:
                act_proj = active_projects(projects)
                print("\n--- Active Projects ---")
                for proj, count in act_proj.items():
                    print(f"{proj}: {count} assigned employees")
            except Exception as e:
                print("Error:", e)

        else:
            print("Invalid choice.")