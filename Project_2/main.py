from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from user_service import UserService
from service_manager import ServiceManager
from booking_service import BookingManager
from database import DatabaseManager

# Initialize
db = DatabaseManager()
db.create_tables()

user_service = UserService()
service_manager = ServiceManager()
booking_manager = BookingManager()


class RequestHandler(BaseHTTPRequestHandler):

    def _send_json(self, data, status=200):
        """Send JSON response with proper status code"""
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def _read_json(self):
        """Read and parse JSON from request body"""
        content_length = self.headers.get('Content-Length')

        if not content_length:
            return None

        try:
            length = int(content_length)
            body = self.rfile.read(length)
            return json.loads(body.decode('utf-8'))
        except (ValueError, json.JSONDecodeError):
            return None

    def _get_id_from_path(self, prefix):
        """Extract ID from URL path like /users/123"""
        try:
            if self.path.startswith(prefix):
                id_part = self.path[len(prefix):].split('/')[0]
                return int(id_part)
        except (ValueError, IndexError):
            pass
        return None

    def do_GET(self):
        """Handle GET requests"""
        try:
            # Root endpoint
            if self.path == "/":
                self._send_json({
                    "message": "Smart Service Management System API",
                    "endpoints": {
                        "users": {
                            "GET /users": "Get all users",
                            "GET /users/<id>": "Get specific user",
                            "POST /users": "Create user",
                            "PUT /users/<id>": "Update user",
                            "DELETE /users/<id>": "Delete user"
                        },
                        "services": {
                            "GET /services": "List all services"
                        },
                        "bookings": {
                            "POST /book": "Create booking",
                            "GET /bookings/user/<id>": "Get user bookings"
                        }
                    }
                })
                return

            # Get all users
            elif self.path == "/users":
                response, status = user_service.get_user()
                self._send_json(response, status)

            # Get specific user
            elif self.path.startswith("/users/"):
                user_id = self._get_id_from_path("/users/")
                if user_id is None:
                    self._send_json({"error": "Invalid user ID"}, 400)
                    return
                response, status = user_service.get_user(user_id)
                self._send_json(response, status)

            # Get all services
            elif self.path == "/services":
                response, status = service_manager.list_services()
                self._send_json(response, status)

            # Get user bookings
            elif self.path.startswith("/bookings/user/"):
                user_id = self._get_id_from_path("/bookings/user/")
                if user_id is None:
                    self._send_json({"error": "Invalid user ID"}, 400)
                    return
                response, status = booking_manager.get_user_bookings(user_id)
                self._send_json(response, status)

            else:
                self._send_json({"error": "Endpoint not found"}, 404)

        except Exception as e:
            self._send_json({"error": str(e)}, 500)

    def do_POST(self):
        """Handle POST requests"""
        try:
            data = self._read_json()

            if data is None:
                self._send_json({"error": "Invalid JSON format"}, 400)
                return

            # Create user
            if self.path == "/users":
                response, status = user_service.create_user(
                    data.get("name"),
                    data.get("email"),
                    data.get("role", "customer")
                )
                self._send_json(response, status)

            # Create booking
            elif self.path == "/book":
                response, status = booking_manager.create_booking(
                    data.get("user_id"),
                    data.get("service_id"),
                    data.get("date")
                )
                self._send_json(response, status)

            else:
                self._send_json({"error": "Endpoint not found"}, 404)

        except Exception as e:
            self._send_json({"error": str(e)}, 500)

    def do_PUT(self):
        """Handle PUT requests"""
        try:
            data = self._read_json()

            if data is None:
                self._send_json({"error": "Invalid JSON format"}, 400)
                return

            # Update user
            if self.path.startswith("/users/"):
                user_id = self._get_id_from_path("/users/")
                if user_id is None:
                    self._send_json({"error": "Invalid user ID"}, 400)
                    return

                response, status = user_service.update_user(user_id, data)
                self._send_json(response, status)

            else:
                self._send_json({"error": "Endpoint not found"}, 404)

        except Exception as e:
            self._send_json({"error": str(e)}, 500)

    def do_DELETE(self):
        """Handle DELETE requests"""
        try:
            # Delete user
            if self.path.startswith("/users/"):
                user_id = self._get_id_from_path("/users/")
                if user_id is None:
                    self._send_json({"error": "Invalid user ID"}, 400)
                    return

                response, status = user_service.delete_user(user_id)
                self._send_json(response, status)

            else:
                self._send_json({"error": "Endpoint not found"}, 404)

        except Exception as e:
            self._send_json({"error": str(e)}, 500)


def run():
    server = HTTPServer(("localhost", 8000), RequestHandler)
    print("=" * 50)
    print("Smart Service Management System")
    print("=" * 50)
    print("Server running at: http://localhost:8000")
    print("\nQuick Test Commands:")
    print('  curl http://localhost:8000/')
    print(
        '  curl -X POST http://localhost:8000/users -H "Content-Type: application/json" -d "{\\"name\\":\\"John\\",\\"email\\":\\"john@test.com\\"}"')
    print('  curl http://localhost:8000/services')
    print("\nPress Ctrl+C to stop")
    print("=" * 50)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✅ Server stopped")


if __name__ == "__main__":
    run()