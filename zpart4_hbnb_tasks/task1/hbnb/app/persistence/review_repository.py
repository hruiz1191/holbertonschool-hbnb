from models.review import Review, db

class ReviewRepository:
    def create(self, review):
        db.session.add(review)
        db.session.commit()
        return review

    def find_by_id(self, review_id):
        return Review.query.get(review_id)

    def find_all(self):
        return Review.query.all()

    def update(self, review):
        db.session.commit()
        return review

    def delete(self, review):
        db.session.delete(review)
        db.session.commit()
