from app import db
from app.models.base_model import BaseModel
from app.models.user import User  

class Review(BaseModel, db.Model):
    """Review model for database."""

    __tablename__ = 'reviews'

    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # Relación con Place
    place_id = db.Column(db.String(60), db.ForeignKey('places.id'), nullable=False)

    # Relación con User
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, text, rating, place, user):
        super().__init__()

        if not isinstance(text, str) or not text.strip():
            raise ValueError("Review text is required")
        self.text = text.strip()

        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        self.rating = rating

        if not place or not getattr(place, 'id', None):
            raise ValueError("Place must be a valid Place instance with id")
        self.place_id = place.id

        if not user or not getattr(user, 'id', None):
            raise ValueError("User must be a valid User instance with id")
        self.user_id = user.id

    def to_dict(self):
        """Devuelve un diccionario del review incluyendo nombre del usuario"""
        user_name = "Anonymous"
        if self.user_id:
            user = User.query.get(self.user_id)
            if user:
                user_name = f"{user.first_name} {user.last_name}".strip() or user.email

        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user_id,
            'user_name': user_name,
            'place_id': self.place_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
      
