import os
import json

user_file = "users.json"

# -------------------------
# CUSTOM EXCEPTIONS
# -------------------------
class LengthBelowEightError(Exception):
    pass


class EmptyStrError(Exception):
    pass


class SpaceError(Exception):
    pass


# -------------------------
# USER CLASS
# -------------------------
class User:

    def __init__(self, username: str, password: str, role: str):
        # FIXED: Use setters to validate
        self.username = username      # Calls setter
        self.password = password      # Calls setter
        self.role = role              # Calls setter

    # -------------------------
    # USERNAME PROPERTY
    # -------------------------
    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value: str):
        if value is None or not isinstance(value, str):
            raise ValueError("Username must be a string.")
        if value.strip() == "":
            raise EmptyStrError("Username cannot be empty.")

        self._username = value.strip()

    # -------------------------
    # PASSWORD PROPERTY
    # -------------------------
    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value: str):
        if value is None:
            raise EmptyStrError("Password cannot be empty.")
        if not isinstance(value, str):
            raise ValueError("Password must be a string.")
        if value == "":
            raise EmptyStrError("Password cannot be an empty string.")
        if len(value) < 8:
            raise LengthBelowEightError(
                "Password must be at least 8 characters long."
            )
        if " " in value:
            raise SpaceError("Password cannot contain spaces.")

        self.__password = value

    # -------------------------
    # ROLE PROPERTY
    # -------------------------
    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value: str):
        allowed = ["Admin", "Manager", "Employee"]

        if value is None or not isinstance(value, str):
            raise ValueError("Role must be a string.")
        if value not in allowed:
            raise ValueError("Invalid role. Choose Admin, Manager, or Employee.")

        self._role = value

    # -------------------------
    # VALIDATE USER
    # -------------------------
    def validate_user(self, username: str, password: str):
        if username != self._username:
            return False, "Username does not match."
        if password != self.__password:
            return False, "Password is incorrect."
        return True, "User validated successfully."

    # -------------------------
    # LOGIN
    # -------------------------
    def login(self, username: str, password: str):
        valid, result = self.validate_user(username, password)
        if not valid:
            return False, f"Login failed: {result}"
        return True, f"Login successful. Welcome, {self.username}!"

    def change_password(self, new_password: str):
        self.password = new_password
        return "Password updated."

    # -------------------------
    # LOAD USER FROM JSON
    # -------------------------
    @staticmethod
    def load():
        users = {}
        if os.path.exists(user_file):
            try:
                with open(user_file, "r") as f:
                    data = json.load(f)
                    for uname, udata in data.items():
                        users[uname] = User(udata["username"], udata["password"], udata["role"])
            except json.JSONDecodeError:
                print("Warning: Users JSON file corrupted.")
        return users

    # -------------------------
    # SAVE USER TO JSON
    # -------------------------
    @staticmethod
    def save(users: dict):
        data = {u.username: {"username": u.username,
                             "password": u.password,
                             "role": u.role}
                for u in users.values()
                }

        with open(user_file, "w") as f:
            json.dump(data, f, indent=4)

        return "User saved successfully."


# -------------------------------------
# CLI FUNCTION
# ------------------------------------
def user_cli(users):
    while True:
        print("""
--- User Management ---
1. Add User
2. Change Password
3. Display Users
0. Back to Main Menu
""")

        choice = input("Enter choice: ")

        if choice == "0":
            break

        elif choice == "1":
            try:
                uname = input("Username: ").strip()
                if uname in users:
                    print("User already exists.")
                    continue

                pwd = input("Password: ")
                role = input("Role (Admin/Manager/Employee): ")

                if role not in ["Admin", "Manager", "Employee"]:
                    print("Invalid role.")
                    continue


                users[uname] = User(uname, pwd, role)
                User.save(users)
                print("User added successfully.")

            except Exception as e:
                print("Error:", e)

        elif choice == "2":
            try:
                uname = input("Username: ")
                user = users.get(uname)

                if not user:
                    print("User not found.")
                    continue

                pwd = input("Current Password: ")
                valid, msg = user.login(uname, pwd)

                if not valid:
                    print(msg)
                    continue

                new_pwd = input("New Password: ")
                user.change_password(new_pwd)
                User.save(users)
                print("Password changed successfully.")

            except Exception as e:
                print("Error:", e)

        elif choice == "3":
            for u in users.values():
                print(f"Username: {u.username}, Role: {u.role}")

        else:
            print("Invalid choice.")