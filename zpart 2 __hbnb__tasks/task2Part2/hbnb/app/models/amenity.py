from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        """Constructor de la clase Amenity"""
        super().__init__()
        self.name = self.validate_string(name, 50)

    def validate_string(self, value, max_length):
        if not isinstance(value, str) or len(value) > max_length:
            raise ValueError(f"Máximo {max_length} caracteres permitidos")
        return value

