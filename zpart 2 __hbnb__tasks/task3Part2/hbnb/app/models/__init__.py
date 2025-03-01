# Archivo app/models/__init__.py
from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

__all__ = ["BaseModel", "User", "Place", "Review", "Amenity"]

