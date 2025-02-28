from .base_model import BaseModel
from .user import User
from .place import Place

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        """Constructor de la clase Review"""
        super().__init__()
        if not isinstance(text, str) or not text.strip():
            raise ValueError("El texto de la reseña es obligatorio")
        self.text = text
        if not (1 <= rating <= 5):
            raise ValueError("El rating debe estar entre 1 y 5")
        self.rating = rating
        if not isinstance(place, Place):
            raise ValueError("El lugar debe ser una instancia de Place")
        self.place = place
        if not isinstance(user, User):
            raise ValueError("El usuario debe ser una instancia de User")
        self.user = user
