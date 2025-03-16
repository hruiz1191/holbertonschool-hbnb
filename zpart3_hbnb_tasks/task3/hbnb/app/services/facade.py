from flask_bcrypt import Bcrypt  # Importar bcrypt para hash de contraseñas
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository

# 🔥 Crear una única instancia del repositorio en memoria para persistencia de datos
bcrypt = Bcrypt()
user_repo = InMemoryRepository()

class HBnBFacade:
    """Main Facade to manage all entities."""

    def __init__(self):
        """Usa la instancia única del repositorio."""
        self.user_repo = user_repo  # 🔥 Reutiliza la misma instancia global
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # ---------------- USERS ----------------
    def get_user_by_email(self, email):
        """Obtiene un usuario por email desde la capa de persistencia."""
        user = self.user_repo.get_user_by_email(email)
        
        if isinstance(user, dict):  # 🔥 Si es un diccionario, conviértelo en un User
            user = User(**user)
    
        return user if isinstance(user, User) else None

    def create_user(self, data):
        """Crea un usuario asegurando que la contraseña se almacene correctamente."""
        if 'password' not in data:
            raise ValueError("Password is required")

        if self.get_user_by_email(data['email']):
            return {'error': 'User already exists'}, 400

        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=hashed_password,
            is_admin=data.get('is_admin', False)
        )
        
        self.user_repo.add(user)
        return user.to_dict(), 201  # 🔥 Ahora devuelve un diccionario

    def get_user(self, user_id):
        """Obtiene un usuario por ID y lo devuelve como diccionario."""
        user = self.user_repo.get(user_id)
        return user.to_dict() if isinstance(user, User) else None

    def get_all_users(self):
        """Obtiene todos los usuarios sin incluir contraseñas."""
        return [user.to_dict() for user in self.user_repo.get_all()]

    def update_user(self, user_id, data):
        """Actualiza un usuario y rehashea la contraseña si se proporciona."""
        user = self.get_user(user_id)
        if not user:
            return None

        for key, value in data.items():
            if key == "password":
                user["password"] = bcrypt.generate_password_hash(value).decode('utf-8')
            else:
                user[key] = value

        return user  # 🔥 Devuelve el usuario actualizado como diccionario

    def delete_user(self, user_id):
        """Elimina un usuario por ID."""
        self.user_repo.delete(user_id)

    # ---------------- PLACES ----------------
    def get_user_by_id(self, user_id):
        """Obtiene un usuario por ID."""
        return self.user_repo.get(user_id)

    def create_place(self, data):
        """Crea un lugar y asigna el propietario autenticado."""
        owner = self.get_user_by_id(data['owner_id'])
        if not owner:
            raise ValueError("Usuario no encontrado")

        place = Place(
            title=data['title'],
            description=data.get('description', ''),
            price=data['price'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            owner=owner  # Pasamos el objeto `User`, no el `owner_id`
        )
        self.place_repo.add(place)
        return place.to_dict()  # 🔥 Convertir a diccionario

    def get_place(self, place_id):
        """Obtiene un lugar por ID."""
        place = self.place_repo.get(place_id)
        return place.to_dict() if place else None

    def get_all_places(self):
        """Recupera todos los lugares registrados y los devuelve como lista de diccionarios."""
        return [place.to_dict() for place in self.place_repo.get_all()]

    def update_place(self, place_id, user_id, data):
        """Actualiza un lugar solo si el usuario autenticado es el dueño."""
        place = self.get_place(place_id)
        if not place or place['owner']['id'] != user_id:
            return None  # No encontrado o no autorizado

        for key, value in data.items():
            place[key] = value

        return place  # 🔥 Devuelve el lugar actualizado como diccionario

    def delete_place(self, place_id, user_id):
        """Elimina un lugar solo si el usuario autenticado es el dueño."""
        place = self.get_place(place_id)
        if not place or place['owner']['id'] != user_id:
            return False  # No encontrado o no autorizado

        self.place_repo.delete(place_id)
        return True

    # ---------------- REVIEWS ----------------
    def create_review(self, data):
        """Crea una reseña validando que no sea el dueño del lugar y que no haya duplicados."""
        user = self.get_user(data['user_id'])
        place = self.get_place(data['place_id'])
        
        if not user or not place:
            raise ValueError("Invalid user_id or place_id")

        if place['owner']['id'] == user['id']:
            raise ValueError("You cannot review your own place")

        if self.get_review_by_user_and_place(user['id'], place['id']):
            raise ValueError("You have already reviewed this place")

        review = Review(
            text=data['text'],
            rating=data['rating'],
            user_id=user['id'],
            place_id=place['id']
        )
        self.review_repo.add(review)
        return review.to_dict()  # 🔥 Convertir a diccionario

    def get_review_by_user_and_place(self, user_id, place_id):
        """Verifica si el usuario ya ha hecho una reseña en ese lugar."""
        for review in self.review_repo.get_all():
            if review.user_id == user_id and review.place_id == place_id:
                return review.to_dict()
        return None

    def get_review(self, review_id):
        """Obtiene una reseña por ID."""
        review = self.review_repo.get(review_id)
        return review.to_dict() if review else None

    def update_review(self, review_id, user_id, data):
        """Permite modificar solo reseñas propias."""
        review = self.get_review(review_id)
        if not review or review['user_id'] != user_id:
            return None  # No encontrado o no autorizado

        for key, value in data.items():
            review[key] = value

        return review  # 🔥 Devuelve la reseña actualizada como diccionario

    def delete_review(self, review_id, user_id):
        """Elimina una reseña solo si es del usuario autenticado."""
        review = self.get_review(review_id)
        if not review or review['user_id'] != user_id:
            return False  # No encontrado o no autorizado

        self.review_repo.delete(review_id)
        return True

    # ---------------- HELPER METHODS ----------------
    def sync_reviews_with_repo(self, place):
        """Sincroniza las reseñas de un lugar con el repositorio."""
        place['reviews'] = [
            r.to_dict() for r in self.review_repo.get_all()
            if r.place_id == place['id']
        ]
        return place
