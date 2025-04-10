from app import db
import uuid
from datetime import datetime

class BaseModel(db.Model):
    __abstract__ = True  # Esto evita que SQLAlchemy cree una tabla para BaseModel directamente

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Actualiza el atributo 'updated_at' y guarda el objeto en la base de datos."""
        self.updated_at = datetime.now()
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """Actualiza los atributos del objeto con los datos proporcionados."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        """
        Convierte el objeto a un diccionario, asegurando que `created_at` y `updated_at`
        no causen un error si por alguna razón son None.
        """
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
