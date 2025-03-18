from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name, id=None, created_at=None, updated_at=None):
        super().__init__(id, created_at, updated_at)
        self.name = self.validate_string(name, 50)

    def validate_string(self, value, max_length):
        if not isinstance(value, str) or len(value) > max_length:
            raise ValueError(f"Máximo {max_length} caracteres permitidos")
        return value

    def to_dict(self):
        base = super().to_dict()
        base.update({'name': self.name})
        return base

    def save(self):
        """Actualizar el timestamp de updated_at"""
        super().save()
