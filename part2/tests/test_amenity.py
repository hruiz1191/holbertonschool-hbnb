import unittest
from app.models.amenity import Amenity

class TestAmenity(unittest.TestCase):
    """Pruebas para la clase Amenity"""

    def test_amenity_creation(self):
        """Verifica que una amenidad se crea correctamente"""
        amenity = Amenity(name="Wi-Fi")
        self.assertEqual(amenity.name, "Wi-Fi")

    def test_invalid_name(self):
        """Verifica que el nombre de la amenidad no supere los 50 caracteres"""
        with self.assertRaises(ValueError):
            Amenity(name="A" * 51)

if __name__ == "__main__":
    unittest.main()
