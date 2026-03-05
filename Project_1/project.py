import csv

project_file = 'project.csv'


class Project:
    def __init__(self, project_id: int, project_name: str):
        self.project_id = project_id
        self.project_name = project_name.strip()
        self.assigned_employee = []
    #------------------------------------
    # PROPERTIES WITH VALIDATION
    #____________________________________

    @property
    def project_id(self):
        return self._project_id

    @project_id.setter
    def project_id(self,value):
        if value is None:
            raise ValueError("Project  ID cannot be None.")
        if not isinstance(value, int):
            raise ValueError("Project ID must be positive integer.")
        if value <= 1000:
            raise   ValueError("Project ID must start with 1000")
        self._project_id = value

    @property
    def project_name(self):
        return self._project_name
    @project_name.setter
    def project_name(self,value):
        if value is None:
            raise ValueError("Project name cannot be None.")
        if not isinstance(value, str)  or not value.strip():
            raise ValueError("Project name must be non - empty string.")
        self._project_name = value

    # -------------------------------
    # METHODS
    # _______________________________
    def assign_employee(self, employee_id: int):
        if not isinstance(employee_id, int) or employee_id <= 0:
            raise ValueError("Employee ID must be a positive integer.")

        if employee_id not in self.assigned_employee:
            self.assigned_employee.append(employee_id)
            return "Employee assigned."
        return "Employee already exists."

    def remove_employee(self, employee_id: int):
        if not isinstance(employee_id, int) or employee_id <= 0:
            raise ValueError("Employee ID must be a positive integer.")

        if employee_id in self.assigned_employee:
            self.assigned_employee.remove(employee_id)
            return "Employee removed."
        return "Employee not found."

    def list_project_members(self):
        return self.assigned_employee

    def to_dict(self):
        return {
            "project_id": self.project_id,
            "project_name": self.project_name,
            "assigned_employee": ",".join(map(str, self.assigned_employee))
        }


# --------------------------------------
# CSV FUNCTIONS
# ---------------------------------------

def save_projects(projects: dict):
    with open(project_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["project_id", "project_name", "assigned_employee"])
        writer.writeheader()
        for p in projects.values():
            writer.writerow(p.to_dict())


def load_projects():
    projects = {}
    try:
        with open(project_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                proj = Project(int(row["project_id"]), row["project_name"])
                if row["assigned_employee"]:
                    proj.assigned_employee = [int(x) for x in row["assigned_employee"].split(",")]
                projects[proj.project_id] = proj
    except FileNotFoundError:
        pass
    except Exception as e:
        print("Error loading projects:", e)

    return projects


# -------------------------------------------
# CLI FUNCTION
# _________________________________________

def project_cli(projects, employees):
    while True:
        print("""
        -----Project Management----
        1. Add Project
        2. Assign Employee
        3. Remove Employee
        4. Display Projects
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
                pid = int(input("Project ID: "))
                if pid in projects:
                    print("Project already exists.")
                    continue
                pname = input("Project Name: ").strip()



                projects[pid] = Project(pid, pname)
                save_projects(projects)
                print("Project added.")

            except Exception as e:
                print("Error:", e)

        elif choice == 2:
            try:
                pid = int(input("Project ID: "))
                proj = projects.get(pid)

                if not proj:
                    print("Project not found.")
                    continue

                eid = int(input("Employee ID: "))
                if eid not in employees:
                    print("Employee not found.")
                    continue

                msg = proj.assign_employee(eid)
                save_projects(projects)
                print(msg)

            except Exception as e:
                print("Error:", e)

        elif choice == 3:
            try:
                pid = int(input("Project ID: "))
                proj = projects.get(pid)

                if not proj:
                    print("Project not found.")
                    continue

                eid = int(input("Employee ID: "))
                msg = proj.remove_employee(eid)
                save_projects(projects)
                print(msg)

            except Exception as e:
                print("Error:", e)

        elif choice == 4:
            try:
                for p in projects.values():
                    print(f"ID: {p.project_id}, Name: {p.project_name}, Employees: {p.assigned_employee}")
            except Exception as e:
                print("Error:", e)

        else:
            print("Invalid choice.")