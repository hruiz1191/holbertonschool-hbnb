from app import db
from app.models.user import User

class UserRepository:
    """Repositorio para operaciones CRUD de usuarios."""

    def get(self, user_id):
        """Busca un usuario por ID."""
        print(f"[USER_REPO] Buscando usuario por ID: {user_id}")
        return User.query.get(user_id)

    def get_all(self):
        """Obtiene todos los usuarios."""
        print("[USER_REPO] Obteniendo todos los usuarios")
        return User.query.all()

    def get_by_email(self, email):
        """Obtiene un usuario por email."""
        print(f"[USER_REPO] Buscando usuario por email: {email}")
        return User.query.filter_by(email=email).first()

    def add(self, user):
        """Agrega un nuevo usuario a la base de datos."""
        print(f"[USER_REPO] Agregando usuario: {user.email}")
        db.session.add(user)
        db.session.commit()
        print("[USER_REPO] Usuario agregado exitosamente")

    def delete(self, user_id):
        """Elimina un usuario por ID."""
        print(f"[USER_REPO] Eliminando usuario ID: {user_id}")
        user = self.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            print("[USER_REPO] Usuario eliminado exitosamente")
            return True
        print("[USER_REPO] Usuario no encontrado para eliminar")
        return False
