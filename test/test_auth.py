
# test_auth.py
# Tests for the authentication and authorization module of the RoomCalc application

import unittest
from auth import create_user, authenticate_user, change_user_password, delete_user, hash_password, verify_password

class TestAuth(unittest.TestCase):

    def test_hash_and_verify_password(self):
        """Test hashing and verifying passwords."""
        password = "secure_password123"
        hashed_password = hash_password(password)
        self.assertTrue(verify_password(hashed_password, password))
        self.assertFalse(verify_password(hashed_password, "wrong_password"))

    def test_create_user(self):
        """Test user creation."""
        create_user("test_user", "test_password")
        self.assertTrue(authenticate_user("test_user", "test_password"))

    def test_authenticate_user(self):
        """Test user authentication."""
        create_user("auth_user", "auth_pass")
        self.assertTrue(authenticate_user("auth_user", "auth_pass"))
        self.assertFalse(authenticate_user("auth_user", "wrong_pass"))

    def test_change_user_password(self):
        """Test changing user password."""
        create_user("change_user", "old_password")
        self.assertTrue(change_user_password("change_user", "old_password", "new_password"))
        self.assertTrue(authenticate_user("change_user", "new_password"))
        self.assertFalse(authenticate_user("change_user", "old_password"))

    def test_delete_user(self):
        """Test deleting a user."""
        create_user("delete_user", "delete_pass")
        self.assertTrue(authenticate_user("delete_user", "delete_pass"))
        delete_user("delete_user")
        self.assertFalse(authenticate_user("delete_user", "delete_pass"))

if __name__ == '__main__':
    unittest.main()

