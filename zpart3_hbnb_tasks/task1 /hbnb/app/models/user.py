import re
from flask_bcrypt import Bcrypt  # Importar bcrypt directamente
from app.models.base_model import BaseModel

# Instancia de bcrypt a nivel de módulo
bcrypt = Bcrypt()

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        """
        Constructor de la clase User.
        - Hashea la contraseña si se proporciona.
        - Valida el email y el nombre.
        """
        super().__init__()
        self.first_name = self.validate_string(first_name, 50)
        self.last_name = self.validate_string(last_name, 50)
        self.email = self.validate_email(email)
        self.is_admin = is_admin
        self.password = self.hash_password(password) if password else None  # Hashea la contraseña si se proporciona

    def validate_string(self, value, max_length):
        """Valida que el string no exceda la longitud máxima."""
        if not isinstance(value, str) or len(value) > max_length:
            raise ValueError(f"Maximum {max_length} characters allowed")
        return value

    def validate_email(self, email):
        """Valida que el email tenga un formato correcto."""
        regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(regex, email):
            raise ValueError("Invalid email format")
        return email

    def hash_password(self, password):
        """Hashea la contraseña antes de almacenarla."""
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifica si la contraseña ingresada coincide con la almacenada."""
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        """Convierte el objeto en un diccionario excluyendo la contraseña."""
        base = super().to_dict()
        base.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        })
        return base  # No devolvemos la contraseña por seguridad
