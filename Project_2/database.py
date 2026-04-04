import sqlite3


class DatabaseManager:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name

    def connect(self):
        """Create and return database connection"""
        try:
            conn = sqlite3.connect(self.db_name)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return None

    def create_tables(self):
        """Create all required tables"""
        conn = self.connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()

            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    role TEXT DEFAULT 'customer'
                )
            ''')

            # Services table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS services (
                    service_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    service_name TEXT NOT NULL,
                    price REAL NOT NULL
                )
            ''')

            # Bookings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bookings (
                    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    service_id INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (service_id) REFERENCES services(service_id)
                )
            ''')

            conn.commit()
            print("✅ Database tables created successfully")
            return True

        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
            return False
        finally:
            conn.close()

    def execute_query(self, query, params=()):
        """Execute INSERT, UPDATE, DELETE queries"""
        conn = self.connect()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Query error: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

    def fetch_data(self, query, params=()):
        """Execute SELECT queries and return data"""
        conn = self.connect()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Fetch error: {e}")
            return None
        finally:
            conn.close()