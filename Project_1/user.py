import os
import json

class LengthBelowEightError(Exception):
    pass

class EmptyStrError(Exception):
    pass

class SpaceError(Exception):
    pass


class User:

    def __init__(self, username: str, password: str, role: str):
        self.set_username(username)
        self.set_password(password)
        self.set_role(role)

    # -------------------------
    # SETTERS
    # -------------------------
    def set_username(self, username: str):
        if username is None or username.strip() == "":
            raise EmptyStrError("Username cannot be empty.")
        if not isinstance(username, str):
            raise ValueError("Username must be a string.")
        self._username = username
        return "Username set successfully."

    def set_password(self, password: str):
        try:
            if password is None:
                raise EmptyStrError("Password cannot be empty.")
            if not isinstance(password, str):
                raise ValueError("Password must be a string.")
            if password == "":
                raise EmptyStrError("Password cannot be an empty string.")
            if len(password) < 8:
                raise LengthBelowEightError("Password must be at least 8 characters long.")
            if " " in password:
                raise SpaceError("Password cannot contain spaces.")

            self.__password = password
            return "Password set successfully."

        except Exception as e:
            return f"Error: {e}"

    def set_role(self, role: str):
        allowed = ["Admin", "Manager", "Employee"]

        if role is None:
            raise ValueError("Role cannot be empty.")
        if not isinstance(role, str):
            raise ValueError("Role must be a string.")
        if role not in allowed:
            raise ValueError("Invalid role. Choose Admin, Manager, or Employee.")

        self._role = role
        return "Role set successfully."

    # -------------------------
    # GETTERS
    # -------------------------
    def get_username(self):
        return self._username

    def get_password(self):
        return self.__password

    def get_role(self):
        return self._role

    # -------------------------
    # VALIDATE USER
    # -------------------------
    def validate_user(self, username: str, password: str):
        if username != self._username:
            return "Username does not match."
        if password != self.__password:
            return "Password is incorrect."
        return "User validated successfully."

    # -------------------------
    # LOGIN
    # -------------------------
    def login(self, username: str, password: str):
        result = self.validate_user(username, password)
        if result != "User validated successfully.":
            return f"Login failed: {result}"
        return f"Login successful. Welcome, {self._username}!"

    # -------------------------
    # SAVE USER TO JSON
    # -------------------------
    def save(self, filename="users.json"):
        data = {}

        if os.path.exists(filename):
            with open(filename, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}

        data[self._username] = {
            "password": self.__password,
            "role": self._role
        }

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

        return f"User '{self._username}' saved successfully."

    # -------------------------
    # LOAD USER FROM JSON
    # -------------------------
    @staticmethod
    def load(username: str, filename="users.json"):
        if not os.path.exists(filename):
            return None, "User file does not exist."

        with open(filename, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return None, "User file is corrupted."

        if username not in data:
            return None, "User not found."

        user_data = data[username]
        user = User(username, user_data["password"], user_data["role"])

        return user, "User loaded successfully."

U = User("bikesh", "Bikesh9090", "Admin")

print(U.login("bikesh", "Bikesh9090"))
print(U.save())  # correct: no filename override
print(U.load("bikesh"))
