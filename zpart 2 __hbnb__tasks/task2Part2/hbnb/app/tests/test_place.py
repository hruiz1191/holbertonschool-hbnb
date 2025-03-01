import unittest
from app.models.place import Place
from app.models.user import User

class TestPlace(unittest.TestCase):
    """Pruebas para la clase Place"""

    def test_place_creation(self):
        """Verifica que un lugar se crea correctamente"""
        owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
        place = Place(title="Cozy Apartment", description="Nice view", price=120.0, latitude=40.7128, longitude=-74.0060, owner=owner)
        self.assertEqual(place.title, "Cozy Apartment")
        self.assertEqual(place.price, 120.0)
        self.assertEqual(place.latitude, 40.7128)
        self.assertEqual(place.longitude, -74.0060)
        self.assertEqual(place.owner, owner)

    def test_invalid_price(self):
        """Verifica que no se pueda asignar un precio negativo"""
        owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
        with self.assertRaises(ValueError):
            Place(title="Cheap Motel", description="Dirty", price=-10.0, latitude=35.0, longitude=139.0, owner=owner)

if __name__ == "__main__":
    unittest.main()
