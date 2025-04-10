from app import db
from app.models.base_model import BaseModel

class Amenity(BaseModel, db.Model):
    """Modelo Amenity adaptado a Base de Datos"""

    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        super().__init__()
        self.name = self.validate_string(name, 50)

    def validate_string(self, value, max_length):
        if not isinstance(value, str) or len(value) > max_length:
            raise ValueError(f"Máximo {max_length} caracteres permitidos")
        return value.strip()

    def to_dict(self):
        """Devuelve un diccionario del objeto"""
        base = super().to_dict()
        base.update({'name': self.name})
        return base
