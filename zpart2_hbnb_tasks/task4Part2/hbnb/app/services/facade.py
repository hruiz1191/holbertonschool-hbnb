from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()

    # -------------------------
    # USERS
    # -------------------------
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_all_users(self):
        return [user.to_dict() for user in self.user_repo.get_all()]

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        user.save()
        return user

    # -------------------------
    # AMENITIES
    # -------------------------
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return [amenity.to_dict() for amenity in self.amenity_repo.get_all()]

    # -------------------------
    # PLACES
    # -------------------------
    def create_place(self, data):
        owner = self.get_user(data['owner_id'])
        if not owner:
            return None

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
            owner=owner
        )
        place.amenities = amenities
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return [place.to_dict() for place in self.place_repo.get_all()]
