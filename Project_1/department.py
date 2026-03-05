import csv
from typing import List, Dict

department_file = "department.csv"


class Department:

    def __init__(self, dept_id: int, dept_name: str):

        self.dept_id = dept_id
        self.dept_name = dept_name.strip()
        self.employee_list: List[int] = []
    #--------------------------------------
    # PROPERTIES WITH VALIDATION
    #____________________________________
    @property
    def dept_id(self):
        return self._dept_id

    @dept_id.setter
    def dept_id(self, value):
        if value is None:
            raise ValueError("Department  ID cannot be None.")
        if not isinstance(value, int):
            raise ValueError("Department ID must be positive integer.")
        if value <= 0:
            raise ValueError("Department ID must start with 1000")
        self._dept_id = value

    @property
    def dept_name(self):
        return self._dept_name

    @dept_name.setter
    def dept_name(self, value):
        if value is None:
            raise ValueError("Department name cannot be None.")
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Department name must be non - empty string.")
        self._dept_name = value

    # ----------------------------------
    # ADD EMPLOYEE LIST
    # ___________________________________

    def add_employee(self, employee_id: int):
        if not isinstance(employee_id, int) or employee_id <= 0:
            raise ValueError("Employee ID must be a positive integer.")
        if employee_id not in self.employee_list:
            self.employee_list.append(employee_id)
            return "Employee added."
        return "Employee already exists."

    def remove_employee(self, employee_id: int):
        if not isinstance(employee_id, int) or employee_id <= 0:
            raise ValueError("Employee ID must be a positive integer.")
        if employee_id in self.employee_list:
            self.employee_list.remove(employee_id)
            return "Employee removed."
        return "Employee not found."

    def total_salary_expense(self, employees: Dict[int, "Employee"]):


        return sum(
            employees[eid].salary
            for eid in self.employee_list
            if eid in employees
        )

    def display_details(self,employees):
        print(f"\nDept ID: {self.dept_id}")
        print(f"Dept Name: {self.dept_name}")

        if self.employee_list:
            names = []
            for eid in self.employee_list:
                if eid in employees:
                    names.append(employees[eid].name)
                else:
                    names.append(f"Unknown({eid})")

            print("Employees:", ", ".join(names))
        else:
            print("Employees: None")


    def to_dict(self):
        return {
            "dept_id": self.dept_id,
            "dept_name": self.dept_name,
            "employee_list": ",".join(map(str, self.employee_list))
        }


# -----------------------------------
# CSV FUNCTIONS
# __________________________________

def gen_dept_from_employee(employees: Dict[int, "Employee"]) -> Dict[int, "Department"]:
    dept_name_to_obj = {}
    next_id = 1
    for emp in employees.values():
        if emp.department not in dept_name_to_obj:
            dept_name_to_obj[emp.department] = Department(next_id, emp.department)
            next_id += 1
        dept_name_to_obj[emp.department].add_employee(emp.employee_id)

    # Convert to proper format with int keys before saving
    dept_by_id = {d.dept_id: d for d in dept_name_to_obj.values()}
    save_dept(dept_by_id)
    return dept_by_id


def save_dept(departments: Dict[int, Department]):
    with open(department_file, "w", newline="") as f:
        import csv
        writer = csv.DictWriter(f, fieldnames=["dept_id", "dept_name", "employee_list"])
        writer.writeheader()
        for dept in departments.values():
            writer.writerow(dept.to_dict())


def load_dept() -> Dict[int, Department]:
    departments = {}
    try:
        with open(department_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                emp_list = [int(x) for x in row["employee_list"].split(",")] if row["employee_list"] else []
                dept = Department(int(row["dept_id"]), row["dept_name"])
                dept.employee_list = emp_list
                departments[dept.dept_id] = dept
    except FileNotFoundError:
        pass
    except Exception as e:
        print("Error:", e)
    return departments


# -----------------------------------
# CLI FUNCTION
# ___________________________________

def department_cli(departments, employees):
    gen_dept_from_employee(employees)
    while True:
        print("""
----- Department Management -----
1. Display Departments
2. Add Department
3. Remove Department
4. Add Employee
5. Remove Employee
6. View Total Salary Expense
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
        # 1. DISPLAY DEPARTMENTS
        # -------------------------
        elif choice == 1:
            try:
                did = input("Department ID (press Enter to show all):").strip()
                #if user presses enter ->show all the department
                if did == "":
                    if not departments:
                        print("No departments available.")
                    else:
                        print("\n--- Department List ---")
                        for d in departments.values():
                            d.display_details(employees)
                            print("-" * 40)
                    continue
                #otherwise ->show specific deparment
                did = int(did)
                dept = departments.get(did)
                if dept:
                    dept.display_details(employees)
                else:
                    print("Department not found.")

            except ValueError as ve:
                print("Invlaid ID input.")
            except Exception as e:
                print("Error:", e)



        # -------------------------
        # 2. ADD DEPARTMENT
        # -------------------------
        elif choice == 2:
            try:
                dept_name = input("New Department Name: ").strip()

                if not dept_name:
                    print("Department name cannot be empty.")
                    continue

                # Check if department already exists
                existing = [d.dept_name for d in departments.values()]
                if dept_name in existing:
                    print("Department already exists.")
                    continue

                # Auto-generate new department ID
                new_id = max(departments.keys(), default=0) + 1
                new_dept = Department(new_id, dept_name)
                departments[new_id] = new_dept
                save_dept(departments)

                print(f"Department '{dept_name}' added successfully.")

            except Exception as e:
                print("Error:", e)

        # -------------------------
        # 3. REMOVE DEPARTMENT
        # -------------------------
        elif choice == 3:
            try:
                did = int(input("Department ID to remove: "))
                dept = departments.get(did)

                if not dept:
                    print("Department not found.")
                    continue

                # Check if department has employees
                if dept.employee_list:
                    print("Cannot delete department with assigned employees.")
                    continue

                del departments[did]
                save_dept(departments)
                print("Department removed successfully.")

            except ValueError:
                print("Invalid input. Enter a valid department ID.")
            except Exception as e:
                print("Error:", e)
        #-----------------------------------
        # Add Employee in Department
        #-----------------------------------

        elif choice == 4:
            try:
                did = int(input("Department ID: "))
                dept = departments.get(did)

                if not dept:
                    print("Department not found.")
                    continue

                eid = int(input("Employee ID: "))
                if eid not in employees:
                    print("Employee not found.")
                    continue

                msg = dept.add_employee(eid)
                save_dept(departments)
                print(msg)

            except Exception as e:
                print("Error:", e)

        #-------------------------------------
        # REMOVE EMPLOYEE from Department
        #-----------------------------------
        elif choice == 5:
            try:
                did = int(input("Department ID: "))
                dept = departments.get(did)

                if not dept:
                    print("Department not found.")
                    continue

                eid = int(input("Employee ID: "))
                msg = dept.remove_employee(eid)
                save_dept(departments)
                print(msg)

            except Exception as e:
                print("Error:", e)

        # -------------------------
        # 4. TOTAL SALARY EXPENSE
        # -------------------------
        elif choice == 6:
            try:
                did_input = input("Department ID (Enter to show all Department.)").strip()
                if did_input == "":
                    if not departments:
                        print("No departments available.")
                    else:
                        print("\n--- Department Salary Expense ---")
                        for d in departments.values():
                            d.total_salary_expense(employees)
                            print("-" * 30)
                    continue
                did = int(did_input)
                dept = departments.get(did)

                if not dept:
                    print("Department not found.")
                else:
                    total = dept.total_salary_expense(employees)
                    print(f"Total salary expense for '{dept.dept_name}': {total}")
                    continue
            except ValueError:
                print("Invalid input. Enter a valid department ID.")
            except Exception as e:
                print("Error:", e)

        else:
            print("Invalid choice.")