
import unittest
import sqlite3
from database import create_connection, execute_sql, create_tables

class TestDatabase(unittest.TestCase):
    def setUp(self):
        """Set up a temporary database for testing."""
        self.database = ":memory:"  # Use an in-memory database for tests
        self.conn = create_connection(self.database)
        create_tables()  # Create tables in the in-memory database

    def tearDown(self):
        """Tear down the test database."""
        self.conn.close()

    def test_connection(self):
        """Test database connection."""
        self.assertIsInstance(self.conn, sqlite3.Connection)

    def test_create_tables(self):
        """Test table creation."""
        # Check if the 'projects' table exists
        table_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='projects'"
        cursor = self.conn.cursor()
        cursor.execute(table_exists)
        table_info = cursor.fetchone()
        self.assertIsNotNone(table_info)

        # Check if the 'rooms' table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='rooms'")
        table_info = cursor.fetchone()
        self.assertIsNotNone(table_info)

        # Check if the 'surfaces' table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='surfaces'")
        table_info = cursor.fetchone()
        self.assertIsNotNone(table_info)

    def test_execute_sql(self):
        """Test SQL execution."""
        sql = "INSERT INTO projects (ProjectName) VALUES ('Test Project')"
        execute_sql(self.conn, sql)
        cursor = self.conn.cursor()
        cursor.execute("SELECT ProjectName FROM projects WHERE ProjectName='Test Project'")
        result = cursor.fetchone()
        self.assertEqual(result[0], 'Test Project')

if __name__ == '__main__':
    unittest.main()
