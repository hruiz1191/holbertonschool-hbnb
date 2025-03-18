from models.amenity import Amenity, db

class AmenityRepository:
    def create(self, amenity):
        db.session.add(amenity)
        db.session.commit()
        return amenity

    def find_by_id(self, amenity_id):
        return Amenity.query.get(amenity_id)

    def find_all(self):
        return Amenity.query.all()

    def update(self, amenity):
        db.session.commit()
        return amenity

    def delete(self, amenity):
        db.session.delete(amenity)
        db.session.commit()
