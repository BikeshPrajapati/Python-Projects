from database import DatabaseManager


class BookingManager:
    def __init__(self):
        self.db = DatabaseManager()

    def create_booking(self, user_id, service_id, date):
        """Create booking with validation"""
        # Validation
        if not user_id or not service_id or not date:
            return {"error": "user_id, service_id, and date are required"}, 400

        # Check user exists
        user = self.db.fetch_data("SELECT * FROM users WHERE id = ?", (user_id,))
        if not user:
            return {"error": "Invalid user ID"}, 404

        # Check service exists
        service = self.db.fetch_data(
            "SELECT * FROM services WHERE service_id = ?",
            (service_id,)
        )
        if not service:
            return {"error": "Invalid service ID"}, 404

        # Create booking
        booking_id = self.db.execute_query(
            "INSERT INTO bookings (user_id, service_id, date) VALUES (?, ?, ?)",
            (user_id, service_id, date)
        )

        if booking_id:
            return {
                "booking_id": booking_id,
                "user_id": user_id,
                "service_id": service_id,
                "date": date
            }, 201

        return {"error": "Failed to create booking"}, 500

    def get_user_bookings(self, user_id):
        """Get all bookings for a specific user with details"""
        # Check user exists
        user = self.db.fetch_data("SELECT * FROM users WHERE id = ?", (user_id,))
        if not user:
            return {"error": "User not found"}, 404

        bookings = self.db.fetch_data('''
            SELECT 
                b.booking_id,
                b.user_id,
                b.service_id,
                b.date,
                u.name as user_name,
                s.service_name,
                s.price
            FROM bookings b
            JOIN users u ON b.user_id = u.id
            JOIN services s ON b.service_id = s.service_id
            WHERE b.user_id = ?
        ''', (user_id,))

        if bookings is None:
            return {"error": "Failed to fetch bookings"}, 500

        return [dict(b) for b in bookings], 200