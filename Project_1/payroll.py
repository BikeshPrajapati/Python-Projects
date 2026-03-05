class Payroll:
    tax_slabs = [
        (50000, 0.05),
        (100000, 0.10),
        (200000, 0.15),
        (float("inf"), 0.20)
    ]

    @staticmethod
    def calculate_tax(salary):
        """Calculate progressive tax with validation."""
        if not isinstance(salary, (int, float)):
            raise TypeError("Salary must be numeric.")
        if salary < 0:
            raise ValueError("Salary cannot be negative.")

        tax = 0
        previous_limit = 0

        for limit, rate in Payroll.tax_slabs:
            if salary > limit:
                # Full bracket is taxed
                tax += (limit - previous_limit) * rate
            else:
                # Only portion in this bracket is taxed
                taxable_amount = max(0, salary - previous_limit)
                tax += taxable_amount * rate
                break
            previous_limit = limit

        return round(tax, 2)

    @staticmethod
    def generate_salary_slip(employee):
        """Generate salary slip with validation."""
        if employee is None:
            raise ValueError("Employee object cannot be None.")
        if not hasattr(employee, "calculate_annual_salary"):
            raise TypeError("Invalid employee object.")

        gross_annual = employee.calculate_annual_salary()
        tax = Payroll.calculate_tax(gross_annual)
        net_annual = gross_annual - tax

        return {
            "Employee": employee.name,
            "Gross Annual": round(gross_annual, 2),
            "Tax": round(tax, 2),
            "Net Amount": round(net_annual, 2)
        }

    @staticmethod
    def deduct_leave(emp_salary, leave_days, total_working_days=30):
        """Deduct salary based on leave days with validation."""
        if not isinstance(emp_salary, (int, float)):
            raise TypeError("Salary must be numeric.")
        if emp_salary < 0:
            raise ValueError("Salary cannot be negative.")
        if not isinstance(leave_days, int):
            raise TypeError("Leave days must be an integer.")
        if leave_days < 0 or leave_days > total_working_days:
            raise ValueError("Leave days must be between 0 and total working days.")

        deduction = (emp_salary / total_working_days) * leave_days
        return round(emp_salary - deduction, 2)


# ---------------------------------------
# CLI FUNCTIONS
# _______________________________________

def payroll_cli(employees):
    while True:
        print("""
        -----Payroll Menu-----
        1. Generate Salary Slip
        2. Deduct Leave
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
                eid = int(input("Employee ID: "))
                emp = employees.get(eid)
                if not emp:
                    print("Employee not found.")
                    continue

                slip = Payroll.generate_salary_slip(emp)
                print("\n--- Salary Slip ---")
                for k, v in slip.items():
                    print(f"{k}: {v}")

            except Exception as e:
                print("Error:", e)

        elif choice == 2:
            try:
                eid = int(input("Employee ID: "))
                emp = employees.get(eid)
                if not emp:
                    print("Employee not found.")
                    continue

                leave_days = int(input("Number of leave days: "))
                deducted_salary = Payroll.deduct_leave(emp.salary, leave_days)

                print(f"\nOriginal salary: {emp.salary}")
                print(f"Salary after leave deduction: {deducted_salary}")

                confirm = input(f"Update base salary to {deducted_salary}? (y/n): ").strip().lower()
                if confirm == 'y':
                    emp.salary = deducted_salary
                    print("Base salary updated.")
                else:
                    print("Salary deduction calculated but not saved.")

            except Exception as e:
                print("Error:", e)

        else:
            print("Invalid choice.")