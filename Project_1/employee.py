import csv
from typing import Dict
from datetime import datetime

employee_file = "employee.csv"


class Employee:
    def __init__(self, employee_id: int, name: str,
                 department: str, salary: float,
                 joining_date: datetime):

        self.employee_id = employee_id
        self.name = name
        self.department = department
        self.salary = salary
        self.joining_date = joining_date

    # -------------------------
    # PROPERTIES WITH VALIDATION
    # -------------------------

    @property
    def employee_id(self):
        return self._employee_id

    @employee_id.setter
    def employee_id(self, value):
        if value is None:
            raise ValueError("Employee ID cannot be None.")
        if not isinstance(value, int):
            raise TypeError("Employee ID must be integer.")
        if value <= 100:
            raise ValueError("Employee ID must be positive and greater than 100.")
        self._employee_id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value is None:
            raise ValueError("Name cannot be None.")
        if not isinstance(value, str):
            raise TypeError("Name must be string.")
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value.strip()

    @property
    def department(self):
        return self._department

    @department.setter
    def department(self, value):
        if value is None:
            raise ValueError("Department cannot be None.")
        if not isinstance(value, str):
            raise TypeError("Department must be string.")
        if not value.strip():
            raise ValueError("Department cannot be empty.")
        self._department = value.strip()

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, value):
        if value is None:
            raise ValueError("Salary cannot be None.")
        if not isinstance(value, (int, float)):
            raise TypeError("Salary must be numeric.")
        if value < 0:
            raise ValueError("Salary cannot be negative.")
        self._salary = float(value)

    @property
    def joining_date(self):
        return self._joining_date

    @joining_date.setter
    def joining_date(self, value):
        if value is None:
            raise ValueError("Joining date cannot be None.")
        if not isinstance(value, datetime):
            raise TypeError("Joining date must be datetime object.")
        self._joining_date = value

    # -------------------------
    # REQUIRED METHODS
    # -------------------------

    def update_salary(self, new_salary: float):
        try:
            self.salary = new_salary
            print(f"Salary updated successfully to {self.salary}")
        except (TypeError, ValueError) as e:
            print(f"Error updating Salary : {e}")

    def calculate_annual_salary(self):
        return self.salary * 12

    def display_details(self):
        print(
            f"Employee ID: {self.employee_id}\n"
            f"Name: {self.name}\n"
            f"Department: {self.department}\n"
            f"Monthly Salary: {self.salary}\n"
            f"Annual Salary: {self.calculate_annual_salary()}\n"
            f"Joining Date: {self.joining_date.strftime('%Y-%m-%d')}"
        )

    def to_dict(self):
        return {
            "employee_id": self.employee_id,
            "name": self.name,
            "department": self.department,
            "salary": self.salary,
            "joining_date": self.joining_date.strftime("%Y-%m-%d")
        }


# -------------------------
# CSV STORAGE METHODS
# -------------------------


def load_employee() -> Dict[int, "Employee"]:
    employees = {}
    try:
        with open(employee_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                emp = Employee(
                    int(row["employee_id"]),
                    row["name"],
                    row["department"],
                    float(row["salary"]),
                    datetime.strptime(row["joining_date"], "%Y-%m-%d")
                )
                employees[emp.employee_id] = emp
    except FileNotFoundError:
        pass
    return employees


def save_employees(employees: Dict[int, "Employee"]):
    with open(employee_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["employee_id", "name", "department", "salary", "joining_date"])
        writer.writeheader()
        for emp in employees.values():
            writer.writerow(emp.to_dict())


# -----------------------------------------
# CLI FUNCTIONS
# _________________________________________

def employee_cli(employees, departments):

    from department import Department, save_dept

    while True:
        print("""
---- Employee Management ----
1. Add Employee
2. Update Salary
3. Display Employee
0. Back to Main Menu
""")

        # Validate menu choice
        try:
            choice = int(input("Choice: "))
        except ValueError:
            print("Invalid input. Enter a number.")
            continue

        # Exit submenu
        if choice == 0:
            break

        # -------------------------
        # 1. ADD EMPLOYEE
        # -------------------------
        elif choice == 1:
            try:
                print("Employee ID start with 100.")
                eid = int(input("Employee ID: "))
                if eid in employees:
                    print("Employee already exists.")
                    continue

                name = input("Name: ").strip()
                dept = input("Department: ").strip()

                # Check if department exists
                existing_departments = [d.dept_name for d in departments.values()]

                if dept not in existing_departments:
                    print(f"Department '{dept}' does not exist.")
                    create = input("Create new department? (y/n): ").strip().lower()

                    if create == "y":
                        # Auto-generate new department ID
                        new_id = max(departments.keys(), default=0) + 1
                        new_dept = Department(new_id, dept)
                        departments[new_id] = new_dept
                        save_dept(departments)
                        print(f"Department '{dept}' created successfully.")
                    else:
                        print("Employee creation cancelled.")
                        continue

                salary = float(input("Salary: "))


                date_input = input("Joining YYYY-MM-DD: ")
                try:
                    join = datetime.strptime(date_input, "%Y-%m-%d")
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD.")
                    continue

                emp = Employee(eid, name, dept, salary, join)
                employees[eid] = emp
                save_employees(employees)
                from Project_1.department import save_dept
                for dept_obj in departments.values():
                    if dept_obj.dept_name == dept:
                        dept_obj.add_employee(eid)
                        save_dept(departments)
                        break

                print("Employee added successfully.")

            except ValueError:
                print("Invalid input. Check numbers and date format.")
            except Exception as e:
                print("Error:", e)

        # -------------------------
        # 2. UPDATE SALARY
        # -------------------------
        elif choice == 2:
            try:
                eid = int(input("Employee ID: "))
                emp = employees.get(eid)

                if not emp:
                    print("Employee not found.")
                    continue

                new_salary = float(input("New salary: "))
                emp.update_salary(new_salary)
                save_employees(employees)

            except ValueError:
                print("Invalid salary input.")
            except Exception as e:
                print("Error:", e)

        # -------------------------
        # 3. DISPLAY EMPLOYEE
        # -------------------------
        elif choice == 3:
            try:
                eid_input = input("Employee ID (press Enter to show all): ").strip()

                # If user presses Enter → show all employees
                if eid_input == "":
                    if not employees:
                        print("No employees found.")
                    else:
                        print("\n--- All Employees ---")
                        for emp in employees.values():
                            emp.display_details()
                            print("---------------------")
                    continue

                # Otherwise → show specific employee
                eid = int(eid_input)
                emp = employees.get(eid)

                if emp:
                    emp.display_details()
                else:
                    print("Employee not found.")

            except ValueError:
                print("Invalid ID input.")
            except Exception as e:
                print("Error:", e)


        else:
            print("Invalid choice.")