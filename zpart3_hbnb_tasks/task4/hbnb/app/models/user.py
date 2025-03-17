import re
import bcrypt  # Importa bcrypt para manejar contraseñas con $2b$
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.base_model import BaseModel

class User(BaseModel):
    """Clase User que extiende BaseModel y gestiona usuarios con autenticación segura."""

    def __init__(self, first_name="", last_name="", email="", password=None, is_admin=False):
        """
        Constructor de la clase User.
        - Valida el email y el nombre.
        - Si la contraseña ya está hasheada, no la vuelve a hashear.
        """
        super().__init__()
        self.first_name = self.validate_string(first_name, 50)
        self.last_name = self.validate_string(last_name, 50)
        self.email = self.validate_email(email)
        self.is_admin = is_admin
        
        # 🔥 Si la contraseña ya está hasheada (bcrypt), no la re-hasheamos
        if password and password.startswith("$2b$"):
            self.password_hash = password  # Ya es un hash bcrypt
        else:
            self.password_hash = self.set_password(password) if password else None  # Almacena el hash

        print(f"[DEBUG] Usuario creado con ID: {self.id}, Email: {self.email}, Admin: {self.is_admin}")

    def validate_string(self, value, max_length):
        """Valida que el string no exceda la longitud máxima y sea válido."""
        if not isinstance(value, str) or len(value) > max_length:
            raise ValueError(f"[ERROR] Máximo {max_length} caracteres permitidos en {value}.")
        return value.strip()

    def validate_email(self, email):
        """Valida que el email tenga un formato correcto."""
        regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(regex, email):
            raise ValueError("[ERROR] Formato de email inválido")
        return email.lower()  # Normaliza el email a minúsculas

    def set_password(self, password):
        """Hashea la contraseña antes de almacenarla."""
        if not password:
            raise ValueError("[ERROR] La contraseña no puede estar vacía")

        hashed = generate_password_hash(password)  # Hash seguro con werkzeug
        print(f"[DEBUG] Password original: {password}")
        print(f"[DEBUG] Password hasheado: {hashed}")  # Verificar que el hash se genera bien
        return hashed

    def verify_password(self, password):
        """Verifica si la contraseña ingresada coincide con el hash almacenado."""
        if not self.password_hash:
            print("[ERROR] No hay contraseña almacenada para este usuario.")
            return False

        # 🔥 Depuración: verifica qué hay en `self.password_hash`
        print(f"[DEBUG] Hash almacenado: {self.password_hash}")

        try:
            # 🔥 Si el hash empieza con $2b$, usa bcrypt para verificarlo
            if self.password_hash.startswith("$2b$"):
                return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

            # Si no es bcrypt, usa werkzeug
            return check_password_hash(self.password_hash, password)

        except ValueError as e:
            print(f"[ERROR] Error al verificar contraseña: {e}")
            return False

    def to_dict(self):
        """Convierte el objeto en un diccionario excluyendo la contraseña por seguridad."""
        base = super().to_dict()
        base.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        })
        print(f"[DEBUG] Convertido a dict: {base}")  # Depuración para verificar estructura
        return base  # 🔥 No devolvemos la contraseña por seguridad
