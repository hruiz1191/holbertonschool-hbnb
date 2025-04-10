from app import db
from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review

# Tabla intermedia para la relación muchos-a-muchos Place <-> Amenity
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(60), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(60), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel, db.Model):
    """Modelo Place adaptado a Base de Datos"""

    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), default="")
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # Relación con User
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)

    # Relaciones con Amenities y Reviews
    amenities = db.relationship('Amenity', secondary=place_amenity, viewonly=False)
    reviews = db.relationship('Review', backref='place', lazy=True)

    def __init__(self, title, description, price, latitude, longitude, owner, amenities=None):
        super().__init__()
        print("[DEBUG] Creando Place...")
        self.title = self.validate_string(title, 100)
        self.description = description if description else ""
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)

        if not isinstance(owner, User):
            print("[ERROR] El owner no es una instancia de User")
            raise ValueError("El owner debe ser una instancia de User")

        self.user_id = owner.id  # Guardamos solo el ID, no el objeto completo
        print(f"[DEBUG] Place creado con user_id={self.user_id}")

        # Inicializar amenities si se pasan
        if amenities:
            for amenity in amenities:
                self.add_amenity(amenity)

    def add_amenity(self, amenity):
        """Agrega un amenity si no está en la lista"""
        if isinstance(amenity, Amenity) and amenity not in self.amenities:
            print(f"[DEBUG] Agregando amenity {amenity.id} al place")
            self.amenities.append(amenity)

    def add_review(self, review):
        """Agrega un review si es válido"""
        if isinstance(review, Review):
            print(f"[DEBUG] Agregando review {review.id} al place")
            self.reviews.append(review)

    def validate_string(self, value, max_length):
        if not isinstance(value, str) or len(value) > max_length:
            print("[ERROR] String de longitud inválida")
            raise ValueError(f"Máximo {max_length} caracteres permitidos")
        return value.strip()

    def validate_price(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            print("[ERROR] Precio inválido")
            raise ValueError("El precio debe ser positivo")
        return float(value)

    def validate_latitude(self, value):
        if not (-90.0 <= value <= 90.0):
            print("[ERROR] Latitud fuera de rango")
            raise ValueError("Latitud fuera de rango")
        return float(value)

    def validate_longitude(self, value):
        if not (-180.0 <= value <= 180.0):
            print("[ERROR] Longitud fuera de rango")
            raise ValueError("Longitud fuera de rango")
        return float(value)

    def to_dict(self):
        """Devuelve un diccionario con todos los campos, incluyendo reviews y amenities"""
        print(f"[DEBUG] Generando dict para Place id={self.id}")
        base = super().to_dict()

        owner_name = "Unknown"
        if self.user_id:
            owner = User.query.get(self.user_id)
            if owner:
                owner_name = f"{owner.first_name} {owner.last_name}".strip() if owner.first_name or owner.last_name else owner.email

        base.update({
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'user_id': self.user_id,
            'user_name': owner_name,  # <-- 🔥 Aquí incluimos el nombre del usuario
            'amenities': [a.to_dict() for a in self.amenities],
            'reviews': [r.to_dict() for r in self.reviews]
        })
        return base
