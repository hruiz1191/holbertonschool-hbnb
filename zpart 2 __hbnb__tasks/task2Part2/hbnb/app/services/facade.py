from app.persistence.repository import InMemoryRepository
from app.models.user import User

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()

    def create_user(self, user_data):
        """Crea un usuario y lo almacena en el repositorio."""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Obtiene un usuario por ID."""
        return self.user_repo.get(user_id)

    def get_all_users(self):
        """Obtiene todos los usuarios almacenados."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Actualiza los datos de un usuario por ID."""
        existing_user = self.get_user(user_id)
        if not existing_user:
            return None
        self.user_repo.update(user_id, user_data)
        return self.get_user(user_id)

