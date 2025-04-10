from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade  # ✅ Importar la instancia de HBnBFacade

api = Namespace('reviews', description='Review management')

# Modelo de Review para validación en Swagger
review_model = api.model('Review', {
    'text': fields.String(required=True, description="Review text"),
    'rating': fields.Integer(required=True, description="Rating (1-5)"),
    'user_id': fields.String(description="User ID (auto-assigned)"),
    'place_id': fields.String(required=True, description="Place ID")
})

# -----------------------------
# Endpoint para listar y crear reviews
# -----------------------------
@api.route('/')
class ReviewList(Resource):
    def get(self):
        """Retrieve all reviews (public endpoint)."""
        reviews = [r.to_dict() for r in facade.review_repo.get_all()]
        return reviews if reviews else {"message": "No reviews found"}, 200

    @jwt_required()
    @api.expect(review_model, validate=True)
    def post(self):
        """Create a new review (Only authenticated users)."""
        user_id = get_jwt_identity()
        data = request.get_json()

        # Validaciones previas
        if not data.get('text') or not data['text'].strip():
            return {"error": "Text cannot be empty"}, 400

        if not (1 <= data.get('rating', 0) <= 5):
            return {"error": "Rating must be between 1 and 5"}, 400

        place = facade.get_place(data['place_id'])
        if not place:
            return {"error": "Place not found"}, 404

        if place["owner"]["id"] == user_id:
            return {"error": "You cannot review your own place"}, 400

        existing_review = facade.get_review_by_user_and_place(user_id, data['place_id'])
        if existing_review:
            return {"error": "You have already reviewed this place"}, 400

        data['user_id'] = user_id  # Asignar ID del usuario autenticado
        review = facade.create_review(data)
        return review, 201


# -----------------------------
# Endpoint para un review específico
# -----------------------------
@api.route('/<string:review_id>')
class ReviewResource(Resource):
    def get(self, review_id):
        """Retrieve a specific review by ID (public endpoint)."""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review, 200

    @jwt_required()
    @api.expect(review_model, validate=True)
    def put(self, review_id):
        """Update an existing review (Owner or Admin)."""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        is_admin = current_user.get("is_admin", False)
        is_owner = review["user_id"] == current_user["id"]

        if not (is_admin or is_owner):
            return {"error": "Unauthorized action"}, 403

        # Actualizar solo los campos permitidos
        updated_data = {key: value for key, value in request.json.items() if key not in ["id", "user_id", "place_id"]}

        updated_review = facade.update_review(review_id, updated_data)
        return {"message": "Review updated successfully", "review": updated_review}, 200

    @jwt_required()
    def delete(self, review_id):
        """Delete a review by ID (Owner or Admin)."""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        is_admin = current_user.get("is_admin", False)
        is_owner = review["user_id"] == current_user["id"]

        if not (is_admin or is_owner):
            return {"error": "Unauthorized action"}, 403

        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200


# -----------------------------
# Endpoint para obtener reviews de un lugar específico
# -----------------------------
@api.route('/places/<string:place_id>/reviews')
class PlaceReviews(Resource):
    def get(self, place_id):
        """Retrieve all reviews for a specific place (public endpoint)."""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        reviews = [r.to_dict() for r in facade.review_repo.get_all() if r.place_id == place_id]
        return reviews if reviews else {"message": "No reviews found for this place"}, 200

