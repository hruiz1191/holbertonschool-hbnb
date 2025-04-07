# app/persistence/user_repository.py
from app.persistence.repository import SQLAlchemyRepository  # Importa SQLAlchemyRepository
from app.models.user import User  # Asegúrate de importar el modelo User
from app import db  # Asegúrate de que db esté importado

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)  # Inicia con el modelo User

    def get_user_by_email(self, email):
        """Obtiene un usuario por su correo electrónico"""
        return self.model.query.filter_by(email=email).first()

