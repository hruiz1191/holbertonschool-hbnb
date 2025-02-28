import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        """Constructor que asigna un UUID y timestamps a cada objeto"""
        self.id = str(uuid.uuid4())  # ID único
        self.created_at = datetime.now()  # Timestamp de creación
        self.updated_at = datetime.now()  # Timestamp de última actualización

    def save(self):
        """Actualiza el timestamp cuando el objeto es modificado"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Actualiza los atributos del objeto basado en un diccionario"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Actualiza `updated_at`
