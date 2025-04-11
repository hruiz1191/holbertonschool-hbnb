import re
from app import db, bcrypt
from app.models.base_model import BaseModel

class User(BaseModel):
    """Modelo de usuario con autenticación segura usando Bcrypt."""

    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)  # Espacio suficiente para hash largo
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship('Place', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    def __init__(self, first_name="", last_name="", email="", password="", is_admin=False):
        super().__init__()
        self.first_name = self._validate_string(first_name, 50)
        self.last_name = self._validate_string(last_name, 50)
        self.email = self._validate_email(email)
        self.is_admin = is_admin
        self.password = self.set_password(password)

    def _validate_string(self, value, max_length):
        """Valida strings de nombres y apellidos."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("[ERROR] Campo obligatorio en string.")
        if len(value) > max_length:
            raise ValueError(f"[ERROR] Máximo {max_length} caracteres permitidos.")
        return value.strip()

    def _validate_email(self, email):
        """Valida formato correcto de email."""
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise ValueError("[ERROR] Formato de email inválido.")
        return email.lower()

    def set_password(self, password):
        """Genera hash de la contraseña solo si no está ya hasheada."""
        if not password:
            raise ValueError("[ERROR] Contraseña requerida.")
        
        if password.startswith('$2b$'):
            print(f"[DEBUG] Password ya viene hasheado (bcrypt): {password[:30]}...")
            return password

        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        print(f"[DEBUG] Password original: '{password}'")
        print(f"[DEBUG] Password hasheado (bcrypt): '{hashed[:30]}...'")
        return hashed

    def verify_password(self, password):
        """Verifica contraseña contra el hash almacenado con DEBUG."""
        if not self.password:
            print("[ERROR] No hay contraseña almacenada para este usuario.")
            return False

        print("\n=== [DEBUG] Verificando contraseña ===")
        print(f"[DEBUG] Contraseña recibida (texto plano): '{password}'")
        print(f"[DEBUG] Hash almacenado en DB: '{self.password[:30]}...'")
        print(f"[DEBUG] Longitud del hash: {len(self.password)} caracteres")
        print(f"[DEBUG] ¿El hash comienza con '$2b$'? {'Sí' if self.password.startswith('$2b$') else 'No'}")

        result = bcrypt.check_password_hash(self.password, password)
        print(f"[DEBUG] Resultado de verificación: {'✅ Correcto' if result else '❌ Falló'}")
        print("=======================================\n")

        return result

    def to_dict(self):
        """Convierte el objeto en un diccionario (sin incluir la contraseña)."""
        base = super().to_dict()
        base.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        })
        return base
