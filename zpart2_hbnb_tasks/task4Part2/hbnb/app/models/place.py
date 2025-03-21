from datetime import datetime
from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = self.validate_string(title, 100)
        self.description = description if description else ""
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)

        if not isinstance(owner, User):
            raise ValueError("El owner debe ser una instancia de User")
        self.owner = owner
        self.amenities = []

    def validate_string(self, value, max_length):
        if not isinstance(value, str) or len(value) > max_length:
            raise ValueError(f"Máximo {max_length} caracteres permitidos")
        return value

    def validate_price(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("El precio debe ser positivo")
        return float(value)

    def validate_latitude(self, value):
        if not (-90.0 <= value <= 90.0):
            raise ValueError("Latitud fuera de rango")
        return float(value)

    def validate_longitude(self, value):
        if not (-180.0 <= value <= 180.0):
            raise ValueError("Longitud fuera de rango")
        return float(value)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner': self.owner.to_dict(),
            'amenities': [a.to_dict() for a in self.amenities],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
