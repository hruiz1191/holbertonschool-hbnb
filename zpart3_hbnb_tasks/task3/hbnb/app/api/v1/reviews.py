from flask import current_app, request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity  # Importar JWT

api = Namespace('reviews', description='Operations related to reviews')

# Modelo de Review para validación en Swagger
review_model = api.model('Review', {
    'text': fields.String(required=True, description="Review text"),
    'rating': fields.Integer(required=True, description="Rating (1-5)"),
    'user_id': fields.String(description="User ID"),  # Se completará automáticamente en el backend
    'place_id': fields.String(description="Place ID")
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

    @jwt_required()  # Solo usuarios autenticados pueden crear reseñas
    @api.expect(review_model, validate=True)
    def post(self):
        """Create a new review."""
        user_id = get_jwt_identity()  # Obtener usuario autenticado
        data = request.get_json()

        # Validaciones previas
        if not data.get('text') or not data['text'].strip():
            return {"error": "Text cannot be empty"}, 400

        if not (1 <= data.get('rating', 0) <= 5):
            return {"error": "Rating must be between 1 and 5"}, 400

        place = current_app.facade.get_place(data['place_id'])
        if not place:
            return {"error": "Place not found"}, 404

        if place.owner_id == user_id:
            return {"error": "You cannot review your own place"}, 400

        existing_review = current_app.facade.get_review_by_user_and_place(user_id, data['place_id'])
        if existing_review:
            return {"error": "You have already reviewed this place"}, 400

        data['user_id'] = user_id  # Asignar ID del usuario autenticado
        review = current_app.facade.create_review(data)
        return review.to_dict(), 201


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

    @jwt_required()  # Solo el autor puede modificar la reseña
    @api.expect(review_model, validate=True)
    def put(self, review_id):
        """Update an existing review."""
        user_id = get_jwt_identity()
        data = request.get_json()
        
        review = current_app.facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        if review.user_id != user_id:
            return {"error": "Unauthorized action"}, 403

        review = current_app.facade.update_review(review_id, data)
        return {"message": "Review updated successfully"}, 200

    @jwt_required()  # Solo el autor puede eliminar la reseña
    def delete(self, review_id):
        """Delete a review by ID."""
        user_id = get_jwt_identity()
        review = current_app.facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        if review.user_id != user_id:
            return {"error": "Unauthorized action"}, 403

        current_app.facade.delete_review(review_id)
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
