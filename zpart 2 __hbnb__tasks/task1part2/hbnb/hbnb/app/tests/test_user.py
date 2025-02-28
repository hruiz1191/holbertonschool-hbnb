import unittest
from app.models.user import User

class TestUser(unittest.TestCase):
    """Pruebas para la clase User"""

    def test_user_creation(self):
        """Verifica que un usuario se crea correctamente con los atributos esperados"""
        user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertFalse(user.is_admin)  # Por defecto, is_admin es False

    def test_email_validation(self):
        """Verifica que el email sea validado correctamente"""
        with self.assertRaises(ValueError):
            User(first_name="Jane", last_name="Doe", email="bademail")

if __name__ == "__main__":
    unittest.main()
