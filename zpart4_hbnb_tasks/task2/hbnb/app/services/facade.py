from flask_bcrypt import Bcrypt
from app import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository  # Usamos SQLAlchemyRepository

# Instancias únicas
bcrypt = Bcrypt()
user_repo = SQLAlchemyRepository(User)
place_repo = SQLAlchemyRepository(Place)
review_repo = SQLAlchemyRepository(Review)
amenity_repo = SQLAlchemyRepository(Amenity)

class HBnBFacade:
    """Fachada que maneja toda la lógica de HBnB."""

    def __init__(self):
        print("[FACADE] Inicializando fachada...")
        self.user_repo = user_repo
        self.place_repo = place_repo
        self.review_repo = review_repo
        self.amenity_repo = amenity_repo

    # --------------- USERS ---------------
    def get_user_by_email(self, email):
        print(f"[FACADE] Buscando usuario por email: {email}")
        return next((user for user in self.user_repo.get_all() if user.email == email), None)

    def get_user(self, user_id):
        print(f"[FACADE] Buscando usuario por ID: {user_id}")
        user = self.user_repo.get(user_id)
        return user.to_dict() if user else None

    def create_user(self, data):
        """Crea usuario nuevo (hasheando contraseña de forma segura)."""
        print(f"[FACADE] Intentando crear usuario: {data.get('email')}")

        if 'password' not in data or not data['password'].strip():
            raise ValueError("[FACADE] Error: Password es obligatorio")

        if self.get_user_by_email(data['email']):
            print("[FACADE] Error: Email ya registrado")
            return {'error': 'User already exists'}, 400

        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        print(f"[FACADE] Password hasheado: {hashed_password}")

        user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=hashed_password,
            is_admin=data.get('is_admin', False)
        )

        self.user_repo.add(user)
        print(f"[FACADE] Usuario creado exitosamente: {user.email}")
        return user.to_dict(), 201

    def get_all_users(self):
        print("[FACADE] Obteniendo todos los usuarios...")
        return [user.to_dict() for user in self.user_repo.get_all()]

    def update_user(self, user_id, data):
        print(f"[FACADE] Actualizando usuario ID: {user_id}")
        user = self.user_repo.get(user_id)
        if not user:
            print("[FACADE] Error: Usuario no encontrado para actualizar.")
            return None

        if 'email' in data or 'password' in data:
            print("[FACADE] Error: No se permite actualizar email o password desde esta función.")
            return {"error": "Cannot update email or password"}, 400

        for key, value in data.items():
            setattr(user, key, value)

        return user.to_dict()

    def delete_user(self, user_id):
        print(f"[FACADE] Eliminando usuario ID: {user_id}")
        user = self.user_repo.get(user_id)
        if not user:
            print("[FACADE] Error: Usuario no encontrado para eliminar.")
            return False

        self.user_repo.delete(user_id)
        print("[FACADE] Usuario eliminado exitosamente.")
        return True

    # --------------- PLACES ---------------
    def create_place(self, data):
        print("[FACADE] Creando un nuevo lugar...")

        # Ahora buscamos con 'user_id'
        owner = self.user_repo.get(data['user_id'])
        if not owner:
            raise ValueError("[FACADE] Error: Usuario propietario no encontrado")

        print(f"[FACADE] Propietario encontrado: {owner.id}")

        place = Place(
            title=data['title'],
            description=data.get('description', ''),
            price=data['price'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            owner=owner  # <<< Pasa el objeto User completo
        )

        self.place_repo.add(place)
        print(f"[FACADE] Lugar '{place.title}' creado exitosamente con ID {place.id}")
        return place.to_dict()

    def get_place(self, place_id):
        print(f"[FACADE] Buscando lugar por ID: {place_id}")
        place = self.place_repo.get(place_id)
        return place.to_dict() if place else None

    def get_all_places(self):
        print("[FACADE] Obteniendo todos los lugares...")
        return [place.to_dict() for place in self.place_repo.get_all()]

    def update_place(self, place_id, user_id, data):
        print(f"[FACADE] Actualizando lugar ID: {place_id}")
        place = self.place_repo.get(place_id)
        if not place:
            print("[FACADE] Error: Lugar no encontrado para actualizar")
            return None

        if place.user_id != user_id:
            print("[FACADE] Error: Solo el propietario puede actualizar")
            return None

        for key, value in data.items():
            if hasattr(place, key):
                setattr(place, key, value)

        print(f"[FACADE] Lugar '{place.title}' actualizado correctamente")
        return place.to_dict()

    def delete_place(self, place_id, user_id):
        print(f"[FACADE] Eliminando lugar ID: {place_id}")
        place = self.place_repo.get(place_id)
        if not place:
            print("[FACADE] Error: Lugar no encontrado para eliminar")
            return False

        if place.user_id != user_id:
            print("[FACADE] Error: Solo el propietario puede eliminar")
            return False

        self.place_repo.delete(place_id)
        print("[FACADE] Lugar eliminado exitosamente")
        return True
    # --------------- REVIEWS ---------------
    def get_review_by_user_and_place(self, user_id, place_id):
        print(f"[FACADE] Buscando reseña para user_id={user_id} y place_id={place_id}")
        return next((review.to_dict() for review in self.review_repo.get_all()
                    if review.user_id == user_id and review.place_id == place_id), None)

    def create_review(self, data):
        print("[FACADE] Creando reseña...")
        user = self.get_user(data['user_id'])
        place = self.get_place(data['place_id'])

        if not user or not place:
            raise ValueError("[FACADE] Usuario o lugar inválido")

        if place['owner']['id'] == user['id']:
            raise ValueError("[FACADE] No puedes reseñar tu propio lugar")

        if self.get_review_by_user_and_place(user['id'], place['id']):
            raise ValueError("[FACADE] Ya has reseñado este lugar")

        if not (1 <= data['rating'] <= 5):
            raise ValueError("[FACADE] La calificación debe ser entre 1 y 5")

        review = Review(
            text=data['text'],
            rating=data['rating'],
            user_id=user['id'],
            place_id=place['id']
        )
        self.review_repo.add(review)
        print("[FACADE] Reseña creada exitosamente")
        return review.to_dict()

    def get_review(self, review_id):
        print(f"[FACADE] Buscando reseña ID: {review_id}")
        review = self.review_repo.get(review_id)
        return review.to_dict() if review else None

    def delete_review(self, review_id, user_id):
        print(f"[FACADE] Eliminando reseña ID: {review_id}")
        review = self.get_review(review_id)
        if not review or review['user_id'] != user_id:
            print("[FACADE] Error: Solo el autor puede eliminar su reseña")
            return False

        self.review_repo.delete(review_id)
        print("[FACADE] Reseña eliminada correctamente.")
        return True

    # --------------- AMENITIES ---------------
    def create_amenity(self, data):
        print("[FACADE] Creando amenidad...")
        if 'name' not in data or not data['name'].strip():
            raise ValueError("[FACADE] El nombre de la amenidad es obligatorio")

        existing = self.amenity_repo.get_all()
        if any(a.name == data['name'] for a in existing):
            raise ValueError("[FACADE] La amenidad ya existe")

        amenity = Amenity(name=data['name'])
        self.amenity_repo.add(amenity)
        print("[FACADE] Amenidad creada exitosamente")
        return amenity.to_dict()

    def get_amenity(self, amenity_id):
        print(f"[FACADE] Buscando amenidad ID: {amenity_id}")
        amenity = self.amenity_repo.get(amenity_id)
        return amenity.to_dict() if amenity else None

    def get_all_amenities(self):
        print("[FACADE] Obteniendo todas las amenidades...")
        return [amenity.to_dict() for amenity in self.amenity_repo.get_all()]

    def update_amenity(self, amenity_id, data):
        print(f"[FACADE] Actualizando amenidad ID: {amenity_id}")
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            print("[FACADE] Error: Amenidad no encontrada")
            return None

        if 'name' in data and data['name'].strip():
            amenity.name = data['name']

        return amenity.to_dict()

    def delete_amenity(self, amenity_id):
        print(f"[FACADE] Eliminando amenidad ID: {amenity_id}")
        return self.amenity_repo.delete(amenity_id)

# Crear instancia global
facade = HBnBFacade()
