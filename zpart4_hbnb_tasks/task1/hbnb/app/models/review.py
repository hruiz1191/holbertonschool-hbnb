from app import db
from app.models.base_model import BaseModel

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
        """Convert review to dictionary."""
        base = super().to_dict()
        base.update({
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place_id,
            'user_id': self.user_id
        })
        return base
