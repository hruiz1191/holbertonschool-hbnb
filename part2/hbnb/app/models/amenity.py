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
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
