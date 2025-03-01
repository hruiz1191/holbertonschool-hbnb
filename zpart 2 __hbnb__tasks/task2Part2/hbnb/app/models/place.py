from app.models.base_model import BaseModel
from .user import User

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        """Constructor de la clase Place"""
        super().__init__()
        self.title = self.validate_string(title, 100)
        self.description = description if description else ""
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        if not isinstance(owner, User):
            raise ValueError("El owner debe ser una instancia de User")
        self.owner = owner
        self.reviews = []
        self.amenities = []

    def validate_string(self, value, max_length):
        if not isinstance(value, str) or len(value) > max_length:
            raise ValueError(f"Máximo {max_length} caracteres permitidos")
        return value

    def validate_price(self, value):
        if value < 0:
            raise ValueError("El precio debe ser un número positivo")
        return float(value)

    def validate_latitude(self, value):
        if not (-90.0 <= value <= 90.0):
            raise ValueError("Latitud fuera de rango (-90 a 90)")
        return value

    def validate_longitude(self, value):
        if not (-180.0 <= value <= 180.0):
            raise ValueError("Longitud fuera de rango (-180 a 180)")
        return value
