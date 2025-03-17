from flask_bcrypt import Bcrypt
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository  # ✅ Solo importamos lo necesario

# ✅ Crear instancias únicas del repositorio en memoria
bcrypt = Bcrypt()
user_repo = InMemoryRepository()
place_repo = InMemoryRepository()
review_repo = InMemoryRepository()
amenity_repo = InMemoryRepository()

class HBnBFacade:
    """Fachada que maneja la lógica del sistema."""

    def __init__(self):
        """Usa las instancias de los repositorios."""
        self.user_repo = user_repo
        self.place_repo = place_repo
        self.review_repo = review_repo
        self.amenity_repo = amenity_repo

    # ---------------- USERS ----------------
    def get_user_by_email(self, email):
        """Obtiene un usuario por email."""
        return next((user for user in self.user_repo.get_all() if user.email == email), None)

    def get_user(self, user_id):
        """Obtiene un usuario por ID."""
        user = self.user_repo.get(user_id)
        return user.to_dict() if user else None

    def create_user(self, data):
        """Crea un usuario con contraseña hasheada."""
        if 'password' not in data or not data['password'].strip():
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
        return user.to_dict(), 201

    def get_all_users(self):
        """Obtiene todos los usuarios sin incluir contraseñas."""
        return [user.to_dict() for user in self.user_repo.get_all()]

    def update_user(self, user_id, data):
        """Actualiza los datos de un usuario."""
        user = self.user_repo.get(user_id)
        if not user:
            return None

        if 'email' in data or 'password' in data:
            return {"error": "Cannot update email or password"}, 400

        for key, value in data.items():
            setattr(user, key, value)

        return user.to_dict()

    def delete_user(self, user_id):
        """Elimina un usuario por ID."""
        user = self.user_repo.get(user_id)
        if not user:
            return False

        self.user_repo.delete(user_id)
        return True

    # ---------------- PLACES ----------------
    def create_place(self, data):
        """Crea un lugar asignando propietario."""
        owner = self.get_user(data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")

        place = Place(
            title=data['title'],
            description=data.get('description', ''),
            price=data['price'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            owner=owner
        )
        self.place_repo.add(place)
        return place.to_dict()

    def get_place(self, place_id):
        """Obtiene un lugar por ID."""
        place = self.place_repo.get(place_id)
        return place.to_dict() if place else None

    def get_all_places(self):
        """Obtiene todos los lugares registrados."""
        return [place.to_dict() for place in self.place_repo.get_all()]

    def update_place(self, place_id, user_id, data):
        """Actualiza un lugar solo si el usuario es el dueño."""
        place = self.get_place(place_id)
        if not place or place['owner']['id'] != user_id:
            return None

        for key, value in data.items():
            setattr(place, key, value)

        return place.to_dict()

    def delete_place(self, place_id, user_id):
        """Elimina un lugar solo si el usuario es el dueño."""
        place = self.get_place(place_id)
        if not place or place['owner']['id'] != user_id:
            return False

        self.place_repo.delete(place_id)
        return True

    # ---------------- REVIEWS ----------------
    def get_review_by_user_and_place(self, user_id, place_id):
        """Verifica si el usuario ya ha hecho una reseña en ese lugar."""
        return next((review.to_dict() for review in self.review_repo.get_all() if review.user_id == user_id and review.place_id == place_id), None)

    def create_review(self, data):
        """Crea una reseña validando usuario, lugar y duplicados."""
        user, place = self.get_user(data['user_id']), self.get_place(data['place_id'])

        if not user or not place:
            raise ValueError("Invalid user_id or place_id")

        if place['owner']['id'] == user['id']:
            raise ValueError("You cannot review your own place")

        if self.get_review_by_user_and_place(user['id'], place['id']):
            raise ValueError("You have already reviewed this place")

        if not (1 <= data['rating'] <= 5):
            raise ValueError("Rating must be between 1 and 5")

        review = Review(
            text=data['text'],
            rating=data['rating'],
            user_id=user['id'],
            place_id=place['id']
        )
        self.review_repo.add(review)
        return review.to_dict()

    def get_review(self, review_id):
        """Obtiene una reseña por ID."""
        review = self.review_repo.get(review_id)
        return review.to_dict() if review else None

    def delete_review(self, review_id, user_id):
        """Elimina una reseña solo si el usuario es el autor."""
        review = self.get_review(review_id)
        if not review or review['user_id'] != user_id:
            return False

        self.review_repo.delete(review_id)
        return True

    # ---------------- AMENITIES ----------------
    def create_amenity(self, data):
        """Crea una nueva amenidad."""
        if 'name' not in data or not data['name'].strip():
            raise ValueError("Amenity name is required")

        existing_amenities = self.amenity_repo.get_all()
        if any(a.name == data['name'] for a in existing_amenities):
            raise ValueError("Amenity already exists")

        amenity = Amenity(name=data['name'])
        self.amenity_repo.add(amenity)  # ✅ Guardar en el repositorio en memoria
        return amenity.to_dict()

    def get_amenity(self, amenity_id):
        """Obtiene una amenidad por ID."""
        amenity = self.amenity_repo.get(amenity_id)
        return amenity.to_dict() if amenity else None

    def get_all_amenities(self):
        """Obtiene todas las amenidades."""
        return [amenity.to_dict() for amenity in self.amenity_repo.get_all()]

    def update_amenity(self, amenity_id, data):
        """Actualiza una amenidad por ID."""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        if 'name' in data and data['name'].strip():
            amenity.name = data['name']

        return amenity.to_dict()

    def delete_amenity(self, amenity_id):
        """Elimina una amenidad por ID."""
        return self.amenity_repo.delete(amenity_id)

# ✅ Crear una instancia global de HBnBFacade
facade = HBnBFacade()

