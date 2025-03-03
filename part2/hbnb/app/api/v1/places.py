"""Places API."""

from flask_restx import Namespace, Resource, fields
from flask import current_app

api = Namespace('places', description='Place operations')

# Modelo de Review (simplificado dentro de Place)
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating (1-5)'),
    'user_id': fields.String(description='User ID')
})

# Modelo de Place extendido con reviews
place_model = api.model('Place', {
    'id': fields.String(),
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'owner_id': fields.String(required=True, description='Owner ID'),
    'amenities': fields.List(fields.String, description='List of amenity IDs'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})


# -----------------------------
# Crear y listar lugares (Places)
# -----------------------------
@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    def post(self):
        """Create a new place."""
        facade = current_app.facade
        try:
            place = facade.create_place(api.payload)
            return place.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400

    def get(self):
        """Retrieve all places."""
        facade = current_app.facade
        places = facade.get_all_places()
        return places, 200


# -----------------------------
# Obtener, actualizar o eliminar un place específico
# -----------------------------
@api.route('/<string:place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        """Retrieve a specific place by ID."""
        facade = current_app.facade
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place.to_dict(), 200

    @api.expect(place_model, validate=True)
    def put(self, place_id):
        """Update an existing place."""
        facade = current_app.facade
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        # Actualiza los atributos (similar a lo que hiciste en el facade)
        for key, value in api.payload.items():
            setattr(place, key, value)

        return {"message": "Place updated successfully"}, 200

    def delete(self, place_id):
        """Delete a place."""
        facade = current_app.facade
        if not facade.get_place(place_id):
            return {"error": "Place not found"}, 404
        facade.delete_place(place_id)
        return {"message": "Place deleted successfully"}, 200
