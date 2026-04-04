from database import DatabaseManager


class UserService:
    def __init__(self):
        self.db = DatabaseManager()

    def create_user(self, name, email, role="customer"):
        """Create new user with validation"""
        # Validation
        if not name or not email:
            return {"error": "Name and email are required"}, 400

        if "@" not in email:
            return {"error": "Invalid email format"}, 400

        # Check duplicate email
        existing = self.db.fetch_data("SELECT * FROM users WHERE email = ?", (email,))
        if existing:
            return {"error": "Email already exists"}, 409

        # Insert user
        user_id = self.db.execute_query(
            "INSERT INTO users (name, email, role) VALUES (?, ?, ?)",
            (name, email, role)
        )

        if user_id:
            return {
                "id": user_id,
                "name": name,
                "email": email,
                "role": role
            }, 201

        return {"error": "Failed to create user"}, 500

    def get_user(self, user_id=None):
        """Get all users or specific user by ID"""
        if user_id:
            users = self.db.fetch_data("SELECT * FROM users WHERE id = ?", (user_id,))
            if not users:
                return {"error": "User not found"}, 404
            return dict(users[0]), 200

        users = self.db.fetch_data("SELECT * FROM users")
        return [dict(u) for u in users], 200

    def update_user(self, user_id, data):
        """Update user information"""
        # Check user exists
        existing = self.db.fetch_data("SELECT * FROM users WHERE id = ?", (user_id,))
        if not existing:
            return {"error": "User not found"}, 404

        # Build update query dynamically
        fields = []
        values = []

        if "name" in data:
            fields.append("name = ?")
            values.append(data["name"])

        if "email" in data:
            # Check duplicate email
            email_check = self.db.fetch_data(
                "SELECT * FROM users WHERE email = ? AND id != ?",
                (data["email"], user_id)
            )
            if email_check:
                return {"error": "Email already exists"}, 409
            fields.append("email = ?")
            values.append(data["email"])

        if "role" in data:
            fields.append("role = ?")
            values.append(data["role"])

        if not fields:
            return {"error": "No fields to update"}, 400

        values.append(user_id)
        query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"

        result = self.db.execute_query(query, tuple(values))

        if result is not None:
            return {"message": f"User {user_id} updated successfully"}, 200

        return {"error": "Failed to update user"}, 500

    def delete_user(self, user_id):
        """Delete user by ID"""
        # Check user exists
        existing = self.db.fetch_data("SELECT * FROM users WHERE id = ?", (user_id,))
        if not existing:
            return {"error": "User not found"}, 404

        result = self.db.execute_query("DELETE FROM users WHERE id = ?", (user_id,))

        if result is not None:
            return {"message": f"User {user_id} deleted successfully"}, 200

        return {"error": "Failed to delete user"}, 500