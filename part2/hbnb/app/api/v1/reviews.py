from flask_restx import Namespace, Resource, fields
from flask import current_app

api = Namespace('reviews', description='Operations about reviews')

# Modelo de Review para validación y documentación en Swagger
review_model = api.model('Review', {
    'text': fields.String(required=True, description="Review text"),
    'rating': fields.Integer(required=True, description="Rating (1-5)"),
    'user_id': fields.String(required=True, description="User ID"),
    'place_id': fields.String(required=True, description="Place ID")
})

# -----------------------------
# Endpoint global para crear y listar todos los reviews
# -----------------------------
@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    def post(self):
        """Create a new review"""
        facade = current_app.facade
        data = api.payload

        # Validaciones
        if not data.get('text') or len(data['text'].strip()) == 0:
            return {"error": "Text cannot be empty"}, 400

        if not (1 <= data.get('rating', 0) <= 5):
            return {"error": "Rating must be between 1 and 5"}, 400

        review = facade.create_review(data)
        if not review:
            return {"error": "Invalid user_id or place_id"}, 400

        return review.to_dict(), 201

    def get(self):
        """Retrieve all reviews"""
        facade = current_app.facade
        reviews = facade.get_all_reviews()

        if not reviews:
            return {"message": "No reviews found"}, 200

        return reviews, 200


# -----------------------------
# Endpoint para acciones sobre un review específico (GET, PUT, DELETE)
# -----------------------------
@api.route('/<string:review_id>')
class ReviewResource(Resource):
    def get(self, review_id):
        """Retrieve a specific review by ID"""
        facade = current_app.facade
        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        return review.to_dict(), 200

    @api.expect(review_model)
    def put(self, review_id):
        """Update an existing review"""
        facade = current_app.facade
        data = api.payload

        # Validaciones básicas
        if not data.get('text') or len(data['text'].strip()) == 0:
            return {"error": "Text cannot be empty"}, 400

        if 'rating' in data and not (1 <= data['rating'] <= 5):
            return {"error": "Rating must be between 1 and 5"}, 400

        review = facade.update_review(review_id, data)

        if not review:
            return {"error": "Review not found"}, 404

        return {"message": "Review updated successfully"}, 200

    def delete(self, review_id):
        """Delete a review by ID"""
        facade = current_app.facade

        if not facade.delete_review(review_id):
            return {"error": "Review not found"}, 404

        return {"message": "Review deleted successfully"}, 200


# -----------------------------
# Endpoint para obtener reviews específicos de un lugar (Place)
# -----------------------------
@api.route('/places/<string:place_id>/reviews')
class PlaceReviews(Resource):
    def get(self, place_id):
        """Retrieve all reviews for a specific place"""
        facade = current_app.facade
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        reviews = facade.get_reviews_by_place(place_id)

        if not reviews:
            return {"message": "No reviews found for this place"}, 200

        return reviews, 200
