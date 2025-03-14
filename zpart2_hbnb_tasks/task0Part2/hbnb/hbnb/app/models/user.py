import re
from app.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        """Constructor de la clase User"""
        super().__init__()  # Llama al constructor de BaseModel
        self.first_name = self.validate_string(first_name, 50)
        self.last_name = self.validate_string(last_name, 50)
        self.email = self.validate_email(email)
        self.is_admin = is_admin  # Booleano

    def validate_string(self, value, max_length):
        """Valida que el string no supere el límite de caracteres"""
        if not isinstance(value, str) or len(value) > max_length:
            raise ValueError(f"El valor debe ser un string con máximo {max_length} caracteres")
        return value

    def validate_email(self, email):
        """Valida el formato del email"""
        regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(regex, email):
            raise ValueError("El email no tiene un formato válido")
        return email
