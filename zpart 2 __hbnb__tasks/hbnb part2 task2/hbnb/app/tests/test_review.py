import unittest
from app.models.review import Review
from app.models.user import User
from app.models.place import Place


class TestReview(unittest.TestCase):
    """Pruebas para la clase Review"""

    def test_review_creation(self):
        """Verifica que una reseña se crea correctamente"""
        user = User(first_name="Mike", last_name="Ross", email="mike.ross@example.com")
        place = Place(title="Modern Loft", description="Spacious", price=200, latitude=48.8566, longitude=2.3522, owner=user)
        review = Review(text="Great stay!", rating=5, place=place, user=user)
        self.assertEqual(review.text, "Great stay!")
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.place, place)
        self.assertEqual(review.user, user)

    def test_invalid_rating(self):
        """Verifica que los valores de rating sean entre 1 y 5"""
        user = User(first_name="Tom", last_name="Ford", email="tom.ford@example.com")
        place = Place(title="Cabin", description="Wooden house", price=90, latitude=55.0, longitude=-3.0, owner=user)
        with self.assertRaises(ValueError):
            Review(text="Bad", rating=6, place=place, user=user)

if __name__ == "__main__":
    unittest.main()
