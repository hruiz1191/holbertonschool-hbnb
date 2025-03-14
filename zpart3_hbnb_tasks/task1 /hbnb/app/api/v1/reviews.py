"""Reviews API."""

from flask import current_app, request
from flask_restx import Namespace, Resource, fields

api = Namespace('reviews', description='Operations related to reviews')

# Modelo de Review para validación en Swagger
review_model = api.model('Review', {
    'text': fields.String(required=True, description="Review text"),
    'rating': fields.Integer(required=True, description="Rating (1-5)"),
    'user_id': fields.String(required=True, description="User ID"),
    'place_id': fields.String(required=True, description="Place ID")
})


# -----------------------------
# Endpoint para listar y crear reviews
# -----------------------------
@api.route('/')
class ReviewList(Resource):
    def get(self):
        """Retrieve all reviews."""
        reviews = current_app.facade.get_all_reviews()
        return reviews if reviews else {"message": "No reviews found"}, 200

    @api.expect(review_model, validate=True)
    def post(self):
        """Create a new review."""
        data = request.get_json()

        # Validaciones previas
        if not data.get('text') or not data['text'].strip():
            return {"error": "Text cannot be empty"}, 400

        if not (1 <= data.get('rating', 0) <= 5):
            return {"error": "Rating must be between 1 and 5"}, 400

        try:
            review = current_app.facade.create_review(data)
            return review.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400


# -----------------------------
# Endpoint para un review específico
# -----------------------------
@api.route('/<string:review_id>')
class ReviewResource(Resource):
    def get(self, review_id):
        """Retrieve a review by ID."""
        review = current_app.facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.to_dict(), 200

    @api.expect(review_model, validate=True)
    def put(self, review_id):
        """Update an existing review."""
        data = request.get_json()

        # Validaciones básicas
        if not data.get('text') or not data['text'].strip():
            return {"error": "Text cannot be empty"}, 400

        if 'rating' in data and not (1 <= data['rating'] <= 5):
            return {"error": "Rating must be between 1 and 5"}, 400

        review = current_app.facade.update_review(review_id, data)
        if not review:
            return {"error": "Review not found"}, 404
        return {"message": "Review updated successfully"}, 200

    def delete(self, review_id):
        """Delete a review by ID."""
        if not current_app.facade.delete_review(review_id):
            return {"error": "Review not found"}, 404
        return {"message": "Review deleted successfully"}, 200


# -----------------------------
# Endpoint para obtener reviews de un lugar específico
# -----------------------------
@api.route('/places/<string:place_id>/reviews')
class PlaceReviews(Resource):
    def get(self, place_id):
        """Retrieve all reviews for a specific place."""
        place = current_app.facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        reviews = current_app.facade.get_reviews_by_place(place_id)
        return reviews if reviews else {"message": "No reviews found for this place"}, 200
