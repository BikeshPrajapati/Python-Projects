from database import DatabaseManager


class ServiceManager:
    def __init__(self):
        self.db = DatabaseManager()

    def add_service(self, service_name, price):
        """Add new service with validation"""
        # Validation
        if not service_name:
            return {"error": "Service name is required"}, 400

        if price is None:
            return {"error": "Price is required"}, 400

        try:
            price = float(price)
            if price < 0:
                return {"error": "Price must be positive"}, 400
        except ValueError:
            return {"error": "Price must be a number"}, 400

        # Insert service
        service_id = self.db.execute_query(
            "INSERT INTO services (service_name, price) VALUES (?, ?)",
            (service_name, price)
        )

        if service_id:
            return {
                "service_id": service_id,
                "service_name": service_name,
                "price": price
            }, 201

        return {"error": "Failed to add service"}, 500

    def list_services(self):
        """Get all services"""
        services = self.db.fetch_data("SELECT * FROM services")

        if services is None:
            return {"error": "Failed to fetch services"}, 500

        return [dict(s) for s in services], 200