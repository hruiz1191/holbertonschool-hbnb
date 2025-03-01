from app.models.review import Review
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        """Inicializa los repositorios en memoria para Users, Amenities, Places y Reviews"""
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # -------------------------
    # USERS (Usuarios)
    # -------------------------
    def create_user(self, user_data):
        """Crea un nuevo usuario y lo almacena en el repositorio"""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Obtiene un usuario por su ID"""
        return self.user_repo.get(user_id)

    def get_all_users(self):
        """Devuelve todos los usuarios en formato de lista de diccionarios"""
        return [user.to_dict() for user in self.user_repo.get_all()]

    # -------------------------
    # AMENITIES (Servicios)
    # -------------------------
    def create_amenity(self, amenity_data):
        """Crea una nueva amenidad y la almacena en el repositorio"""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Obtiene una amenidad por su ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Devuelve todas las amenidades en formato de lista de diccionarios"""
        return [amenity.to_dict() for amenity in self.amenity_repo.get_all()]

    def delete_amenity(self, amenity_id):
        """Elimina una amenidad si existe"""
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            self.amenity_repo.delete(amenity_id)
            return True
        return False

    # -------------------------
    # PLACES (Lugares)
    # -------------------------
    def create_place(self, data):
        """Crea un nuevo lugar con amenities y lo almacena en el repositorio"""
        owner = self.get_user(data['owner_id'])
        if not owner:
            return None  # ❌ Evita crear un lugar sin dueño válido

        # Asocia amenities al lugar
        amenities = []
        for amenity_id in data.get('amenities', []):
            amenity = self.get_amenity(amenity_id)
            if amenity:
                amenities.append(amenity)

        place = Place(
            title=data['title'],
            description=data.get('description', ''),
            price=data['price'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            owner=owner,
            amenities=amenities
        )

        # ✅ Inicializa la lista de reviews vacía
        place.reviews = []

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Obtiene un lugar por su ID"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Devuelve todos los lugares en formato de lista de diccionarios"""
        return [place.to_dict() for place in self.place_repo.get_all()]

    def delete_place(self, place_id):
        """Elimina un lugar si existe"""
        place = self.place_repo.get(place_id)
        if place:
            self.place_repo.delete(place_id)
            return True
        return False

    # -------------------------
    # REVIEWS (Reseñas)
    # -------------------------
    def create_review(self, review_data):
        """Crea un nuevo review asociado a un lugar y usuario"""
        user = self.get_user(review_data['user_id'])
        place = self.get_place(review_data['place_id'])

        if not user or not place:
            return None  # ❌ Evita crear un review sin usuario o lugar válido

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place=place,
            user=user
        )

        self.review_repo.add(review)

        # ✅ Verificar que `place.reviews` existe antes de añadir el review
        if not hasattr(place, 'reviews'):
            place.reviews = []

        place.reviews.append(review)

        return review

    def get_review(self, review_id):
        """Obtiene un review por su ID"""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Devuelve todos los reviews en formato de lista de diccionarios"""
        return [review.to_dict() for review in self.review_repo.get_all()]

    def get_reviews_by_place(self, place_id):
        """Devuelve todos los reviews asociados a un lugar"""
        place = self.get_place(place_id)
        if not place:
            return []  # ✅ Retorna lista vacía en lugar de None
        return [review.to_dict() for review in place.reviews]

    def delete_review(self, review_id):
        """Elimina un review y lo elimina de la lista de reviews del lugar"""
        review = self.review_repo.get(review_id)
        if not review:
            return False

        # ✅ Verifica que `place.reviews` existe antes de intentar modificarlo
        if hasattr(review.place, 'reviews'):
            review.place.reviews = [r for r in review.place.reviews if r.id != review_id]

        self.review_repo.delete(review_id)
        return True

