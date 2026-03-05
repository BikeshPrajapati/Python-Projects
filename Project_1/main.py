from user import *
from employee import *
from department import *
from project import *
from payroll import *
from report import *


def main():

    # Load all stored data
    users = User.load()
    employees = load_employee()
    departments = load_dept()
    projects = load_projects()

    logged_in_user = None

    while True:
        print("""
======== ERMS SYSTEM ========
1. Login
2. Employee Management
3. Department Management
4. Project Assignment
5. Payroll Processing
6. Generate Reports
7. User Management
8. Exit
=============================
""")

        # Validate main menu choice
        try:
            choice = int(input("Choice: "))
        except ValueError:
            print("Invalid input. Enter a number.")
            continue

        # -----------------------------
        # 8. EXIT SYSTEM
        # -----------------------------
        if choice == 8:
            print("Exiting system...")
            break

        # -----------------------------
        # 1. LOGIN
        # -----------------------------
        # 1. LOGIN
        elif choice == 1:
            while True:
                uname = input("Username: ").strip()
                pwd = input("Password: ")

                user = users.get(uname)

                # If user does NOT exist → ask what to do
                if not user:
                    print("User not found.")

                    while True:
                        action = input("Do you want to (T)ry again or (C)reate a new user? ").strip().lower()

                        if action == "t":
                            # Restart login process
                            break

                        elif action == "c":
                            # Create new user
                            while True:
                                role = input("Assign role (Admin/Manager/Employee): ").strip()
                                if role in ["Admin", "Manager", "Employee"]:
                                    break
                                print("Invalid role. Try again.")

                            try:
                                new_user = User(uname, pwd, role)
                                users[uname] = new_user
                                User.save(users)
                                print("New user created successfully.")
                                logged_in_user = new_user
                            except Exception as e:
                                print("Error creating user:", e)

                            break  # Exit login loop after creation

                        else:
                            print("Invalid choice. Enter T or C.")

                    continue  # Restart main menu loop

                # If user exists → validate login
                valid, msg = user.login(uname, pwd)
                print(msg)

                if not valid:
                    continue

                logged_in_user = user
                break

        # -----------------------------
        # REQUIRE LOGIN FOR OPTIONS 2–7
        # -----------------------------
        elif choice in [2, 3, 4, 5, 6]:
            if not logged_in_user:
                print("You must login first.")
                continue

            # -----------------------------
            # 2. EMPLOYEE MANAGEMENT
            # -----------------------------
            if choice == 2:
                try:
                    employee_cli(employees, departments)
                    save_employees(employees)
                except Exception as e:
                    print("Error:", e)

            # -----------------------------
            # 3. DEPARTMENT MANAGEMENT
            # -----------------------------
            elif choice == 3:
                try:
                    department_cli(departments, employees)
                    save_dept(departments)
                except Exception as e:
                    print("Error:", e)

            # -----------------------------
            # 4. PROJECT ASSIGNMENT
            # -----------------------------
            elif choice == 4:
                try:
                    project_cli(projects, employees)
                    save_projects(projects)
                except Exception as e:
                    print("Error:", e)

            # -----------------------------
            # 5. PAYROLL PROCESSING
            # -----------------------------
            elif choice == 5:
                try:
                    payroll_cli(employees)
                    save_employees(employees)
                except Exception as e:
                    print("Error:", e)

            # -----------------------------
            # 6. REPORTING
            # -----------------------------
            elif choice == 6:
                try:
                    reporting_cli(employees, departments, projects)
                except Exception as e:
                    print("Error:", e)

        # -----------------------------
        # 7. USER MANAGEMENT (NEW)
        # -----------------------------
        elif choice == 7:
            try:
                user_cli(users)
                    # User.save(users) is called inside user_cli
            except Exception as e:
                print("Error:", e)

        else:
            print("Invalid choice.")

    # Save everything before exit
    save_employees(employees)
    save_dept(departments)
    save_projects(projects)
    print("All data saved. Goodbye!")


if __name__ == "__main__":
    main()