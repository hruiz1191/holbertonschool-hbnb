import re
from app import db, bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.base_model import BaseModel

class User(BaseModel):
    """Clase User que extiende BaseModel y gestiona usuarios con autenticación segura."""

    __tablename__ = 'users'  # Nombre de la tabla en la base de datos

    # Definición de columnas en la base de datos
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)  # Aquí guardamos la contraseña hasheada
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name="", last_name="", email="", password=None, is_admin=False):
        """
        Constructor de la clase User.
        - Valida el email y el nombre.
        - Si la contraseña ya está hasheada (bcrypt), no la re-hasheamos.
        """
        super().__init__()  # Llama al constructor de BaseModel
        self.first_name = self.validate_string(first_name, 50)
        self.last_name = self.validate_string(last_name, 50)
        self.email = self.validate_email(email)
        self.is_admin = is_admin

        # Si la contraseña ya está hasheada (bcrypt) ("$2b$" en werkzeug genera $pbkdf2$, 
        # pero si estás usando la librería 'bcrypt' directamente, también verás "$2b$")
        if password and password.startswith("$2b$"):
            self.password = password  # Asumimos que ya viene hasheada
        else:
            # Si no viene hasheada, la generamos
            self.password = self.set_password(password) if password else None

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
        print(f"[DEBUG] Password hasheado: {hashed}")
        return hashed

    def verify_password(self, password):
        """
        Verifica si la contraseña ingresada coincide con el hash almacenado
        en self.password.
        """
        if not self.password:
            print("[ERROR] No hay contraseña almacenada para este usuario.")
            return False

        # Depuración: verifica qué hay en `self.password`
        print(f"[DEBUG] Hash almacenado: {self.password}")

        try:
            # Si el hash empieza con '$2b$', utilizamos bcrypt.checkpw
            # NOTA: Si generas el hash con 'werkzeug', no necesariamente es bcrypt "$2b$".
            #       Werkzeug por defecto usa pbkdf2:sha256.
            if self.password.startswith("$2b$"):
                return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
            
            # Si no empieza con '$2b$', usamos la función de werkzeug
            return check_password_hash(self.password, password)

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
            # 'password' no se añade intencionalmente para no exponerla
        })
        print(f"[DEBUG] Convertido a dict: {base}")
        return base

