"""Review model."""

from app.models.base_model import BaseModel
from app.models.user import User


class Review(BaseModel):
    """Review entity."""

    def __init__(self, text, rating, place, user):
        """Initialize a review."""
        super().__init__()

        if not isinstance(text, str) or not text.strip():
            raise ValueError("Review text is required")
        self.text = text

        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        self.rating = rating

        # Importación diferida para evitar import circular
        from app.models.place import Place

        if not isinstance(place, Place):
            raise ValueError("Place must be a valid Place instance")
        self.place = place

        if not isinstance(user, User):
            raise ValueError("User must be a valid User instance")
        self.user = user

    def to_dict(self):
        """Convert review to dictionary."""
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place.id,
            'user_id': self.user.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
