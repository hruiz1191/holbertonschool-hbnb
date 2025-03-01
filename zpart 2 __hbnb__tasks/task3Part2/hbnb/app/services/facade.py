from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()  # Añadimos repositorio para amenities

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        existing_amenity = self.get_amenity(amenity_id)
        if not existing_amenity:
            return None
        if 'name' in amenity_data:
            existing_amenity.name = existing_amenity.validate_string(amenity_data['name'], 50)
        self.amenity_repo.update(amenity_id, existing_amenity.__dict__)
        return self.get_amenity(amenity_id)
