from flask_bcrypt import Bcrypt  # Importar bcrypt directamente
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository

# Crear una instancia local de bcrypt
bcrypt = Bcrypt()

class HBnBFacade:
    """Main Facade to manage all entities."""

    def __init__(self):
        """Initialize all in-memory repositories."""
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # ---------------- USERS ----------------
    def create_user(self, data):
        """Crea un usuario asegurando que la contraseña se almacene correctamente."""
        if 'password' not in data:
            raise ValueError("Password is required")

        # Hashear la contraseña antes de crear el usuario
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=hashed_password,  
            is_admin=data.get('is_admin', False)
        )
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Obtiene un usuario por ID."""
        return self.user_repo.get(user_id)

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
                user.password = bcrypt.generate_password_hash(value).decode('utf-8')  # Hashea la nueva contraseña
            else:
                setattr(user, key, value)

        return user

    def delete_user(self, user_id):
        """Elimina un usuario por ID."""
        self.user_repo.delete(user_id)

    # ---------------- AMENITIES ----------------
    def create_amenity(self, data):
        amenity = Amenity(**data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return [a.to_dict() for a in self.amenity_repo.get_all()]

    def delete_amenity(self, amenity_id):
        self.amenity_repo.delete(amenity_id)

    def update_amenity(self, amenity_id, data):
        """Actualiza un amenity por ID."""
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        amenity.name = data.get('name', amenity.name)
        amenity.save()  # Actualiza updated_at
        return amenity

    # ---------------- PLACES ----------------
    def create_place(self, data):
        owner = self.get_user(data['owner_id'])
        if not owner:
            raise ValueError("Invalid owner_id")

        amenities = []
        for amenity_id in data.get('amenities', []):
            amenity = self.get_amenity(amenity_id)
            if amenity:
                amenities.append(amenity)
            else:
                print(f"⚠️ Amenity {amenity_id} no encontrado. Será ignorado.")

        place = Place(
            title=data['title'],
            description=data.get('description', ''),
            price=data['price'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            owner=owner
        )
        place.amenities = amenities
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if place:
            self.sync_reviews_with_repo(place)
        return place

    def get_all_places(self):
        places = self.place_repo.get_all()
        for place in places:
            self.sync_reviews_with_repo(place)
        return [place.to_dict() for place in places]

    def delete_place(self, place_id):
        self.place_repo.delete(place_id)

    def sync_reviews_with_repo(self, place):
        place.reviews = [
            r for r in self.review_repo.get_all()
            if r.place.id == place.id
        ]

    # ---------------- REVIEWS ----------------
    def create_review(self, data):
        user = self.get_user(data['user_id'])
        place = self.get_place(data['place_id'])
        if not user or not place:
            raise ValueError("Invalid user_id or place_id")

        review = Review(
            text=data['text'],
            rating=data['rating'],
            user=user,
            place=place
        )
        self.review_repo.add(review)
        self.sync_reviews_with_repo(place)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return [r.to_dict() for r in self.review_repo.get_all()]

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            return []
        return [r.to_dict() for r in place.reviews]

    def update_review(self, review_id, data):
        review = self.get_review(review_id)
        if not review:
            return None
        for key, value in data.items():
            setattr(review, key, value)
        self.sync_reviews_with_repo(review.place)
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if review:
            review.place.reviews = [
                r for r in review.place.reviews if r.id != review_id
            ]
            self.review_repo.delete(review_id)
            return True
        return False
