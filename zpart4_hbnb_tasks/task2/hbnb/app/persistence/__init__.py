# app/persistence/__init__.py
from .repository import Repository, SQLAlchemyRepository  # Importa SQLAlchemyRepository
from .user_repository import UserRepository  # Importa UserRepository

__all__ = ['Repository', 'SQLAlchemyRepository', 'UserRepository']  # Actualiza __all__ para incluir UserRepository

