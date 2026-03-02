import csv
from datetime import datetime


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
        if value <= 0:
            raise ValueError("Employee ID must be positive.")
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
            print (f"Error updateing Salary : {e}")

    def calculate_annual_salary(self):
        return self.salary * 12

    def display_details(self):
        print(f"""
                Employee ID: {self.employee_id}
                Name: {self.name}
                Department: {self.department}
                Monthly Salary: {self.salary}
                Annual Salary: {self.calculate_annual_salary()}
                Joining Date: {self.joining_date.strftime("%Y-%m-%d")}
        """)

    # -------------------------
    # CSV STORAGE METHODS
    # -------------------------

    def to_dict(self):
        return {
            "employee_id": self.employee_id,
            "name": self.name,
            "department": self.department,
            "salary": self.salary,
            "joining_date": self.joining_date.strftime("%Y-%m-%d")
        }

    @staticmethod
    def save_to_csv(employee, filename="employees.csv"):
        file_exists = False
        try:
            with open(filename, "r"):
                file_exists = True
        except FileNotFoundError:
            pass

        with open(filename, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=employee.to_dict().keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(employee.to_dict())