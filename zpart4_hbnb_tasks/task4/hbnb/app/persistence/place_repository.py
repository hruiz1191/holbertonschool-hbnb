from models.place import Place, db

class PlaceRepository:
    def create(self, place):
        db.session.add(place)
        db.session.commit()
        return place

    def find_by_id(self, place_id):
        return Place.query.get(place_id)

    def find_all(self):
        return Place.query.all()

    def update(self, place):
        db.session.commit()
        return place

    def delete(self, place):
        db.session.delete(place)
        db.session.commit()
