from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade  # Instancia del sistema HBnB

# Namespace para Reviews
reviews_ns = Namespace('reviews', description='Review management')

# Modelo de datos para Swagger y validación
review_model = reviews_ns.model('Review', {
    'text': fields.String(required=True, description="Review text"),
    'rating': fields.Integer(required=True, description="Rating (1-5)"),
    'user_id': fields.String(description="User ID (auto-assigned)"),
    'place_id': fields.String(description="Place ID")  # <<<< SIN required=True
})

# -----------------------------
# Endpoint para listar y crear Reviews generales
# -----------------------------
@reviews_ns.route('/')
class ReviewList(Resource):
    def get(self):
        """Retrieve all reviews (public endpoint)."""
        print("[DEBUG] Solicitando lista de todos los reviews...")
        reviews = [r.to_dict() for r in facade.review_repo.get_all()]
        if reviews:
            print(f"[SUCCESS] Reviews encontrados: {reviews}")
            return reviews, 200
        else:
            print("[INFO] No se encontraron reviews.")
            return {"message": "No reviews found"}, 200

    @jwt_required()
    @reviews_ns.expect(review_model, validate=True)
    def post(self):
        """Create a new review (authenticated users only)."""
        user_id = get_jwt_identity()
        data = request.get_json()
        print(f"[DEBUG] Creando review. Datos recibidos: {data}")

        # Validaciones
        if not data.get('text') or not data['text'].strip():
            print("[ERROR] El texto del review es vacío.")
            return {"error": "Text cannot be empty"}, 400

        if not (1 <= data.get('rating', 0) <= 5):
            print("[ERROR] Rating inválido.")
            return {"error": "Rating must be between 1 and 5"}, 400

        place = facade.get_place(data['place_id'])
        if not place:
            print("[ERROR] Place no encontrado.")
            return {"error": "Place not found"}, 404

        if place['user_id'] == user_id:
            print("[ERROR] Usuario intentando reseñar su propio lugar.")
            return {"error": "You cannot review your own place"}, 400

        existing_review = facade.get_review_by_user_and_place(user_id, data['place_id'])
        if existing_review:
            print("[ERROR] Usuario ya reseñó este lugar.")
            return {"error": "You have already reviewed this place"}, 400

        data['user_id'] = user_id
        review = facade.create_review(data)
        print(f"[SUCCESS] Review creado: {review}")
        return review, 201

# -----------------------------
# Endpoint para un Review específico (por ID)
# -----------------------------
@reviews_ns.route('/<string:review_id>')
class ReviewResource(Resource):
    def get(self, review_id):
        """Retrieve a specific review by ID."""
        print(f"[DEBUG] Buscando review ID: {review_id}")
        review = facade.get_review(review_id)
        if not review:
            print("[ERROR] Review no encontrado.")
            return {"error": "Review not found"}, 404
        print(f"[SUCCESS] Review encontrado: {review}")
        return review, 200

    @jwt_required()
    @reviews_ns.expect(review_model, validate=True)
    def put(self, review_id):
        """Update an existing review (owner only)."""
        current_user_id = get_jwt_identity()
        print(f"[DEBUG] Actualizando review ID: {review_id}")
        review = facade.get_review(review_id)

        if not review:
            print("[ERROR] Review no encontrado para actualizar.")
            return {"error": "Review not found"}, 404

        if review['user_id'] != current_user_id:
            print("[ERROR] Usuario no autorizado para actualizar este review.")
            return {"error": "Unauthorized action"}, 403

        updated_data = {key: value for key, value in request.json.items() if key not in ["id", "user_id", "place_id"]}
        updated_review = facade.update_review(review_id, updated_data)
        print(f"[SUCCESS] Review actualizado: {updated_review}")
        return {"message": "Review updated successfully", "review": updated_review}, 200

    @jwt_required()
    def delete(self, review_id):
        """Delete a review (owner only)."""
        current_user_id = get_jwt_identity()
        print(f"[DEBUG] Eliminando review ID: {review_id}")
        review = facade.get_review(review_id)

        if not review:
            print("[ERROR] Review no encontrado para eliminar.")
            return {"error": "Review not found"}, 404

        if review['user_id'] != current_user_id:
            print("[ERROR] Usuario no autorizado para eliminar este review.")
            return {"error": "Unauthorized action"}, 403

        facade.delete_review(review_id)
        print("[SUCCESS] Review eliminado correctamente.")
        return {"message": "Review deleted successfully"}, 200

# -----------------------------
# Alias: Reviews por Place ID (GET/POST)
# -----------------------------
@reviews_ns.route('/<string:place_id>')
class PlaceReviews(Resource):
    def get(self, place_id):
        """Retrieve all reviews for a specific place."""
        print(f"[DEBUG] Buscando reviews para el lugar ID: {place_id}")
        place = facade.get_place(place_id)
        if not place:
            print("[ERROR] Lugar no encontrado.")
            return {"error": "Place not found"}, 404

        reviews = facade.get_reviews_by_place(place_id)
        if not reviews:
            print("[INFO] No hay reviews para este lugar.")
            return {"message": "No reviews found for this place"}, 200

        reviews_list = [review.to_dict() for review in reviews]
        print(f"[SUCCESS] Reviews encontrados: {reviews_list}")
        return reviews_list, 200

    @jwt_required()
    @reviews_ns.expect(review_model, validate=True)
    def post(self, place_id):
        """Create a review for a specific place (authenticated users only)."""
        user_id = get_jwt_identity()
        data = request.get_json()
        print(f"[DEBUG] Intentando crear review para place ID {place_id} con datos {data}")

        place = facade.get_place(place_id)
        if not place:
            print("[ERROR] Lugar no encontrado para review.")
            return {"error": "Place not found"}, 404

        if place['user_id'] == user_id:
            print("[ERROR] Usuario intentando reseñar su propio lugar.")
            return {"error": "You cannot review your own place"}, 400

        existing_review = facade.get_review_by_user_and_place(user_id, place_id)
        if existing_review:
            print("[ERROR] Ya existe un review del usuario para este lugar.")
            return {"error": "You have already reviewed this place"}, 400

        data['user_id'] = user_id
        data['place_id'] = place_id
        review = facade.create_review(data)
        print(f"[SUCCESS] Review creado: {review}")
        return review, 201
