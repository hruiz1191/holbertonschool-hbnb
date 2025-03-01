from app.models.base_model import BaseModel
from app.models.user import User

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

        # 🔥 Importación diferida para evitar importación circular con Place
        from app.models.place import Place  

        if not isinstance(place, Place):
            raise ValueError("El lugar debe ser una instancia de Place")
        self.place = place

        if not isinstance(user, User):
            raise ValueError("El usuario debe ser una instancia de User")
        self.user = user

    def to_dict(self):
        """Convierte el review en un diccionario para serialización"""
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place.id,
            'user_id': self.user.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
