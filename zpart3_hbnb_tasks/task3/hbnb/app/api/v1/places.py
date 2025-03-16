from flask_restx import Namespace, Resource, fields
from flask import current_app
from flask_jwt_extended import jwt_required, get_jwt_identity  # Importar JWT

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
    'owner': fields.Nested(api.model('Owner', {
        'id': fields.String(description='Owner ID'),
        'first_name': fields.String(description='Owner first name'),
        'last_name': fields.String(description='Owner last name'),
        'email': fields.String(description='Owner email')
    }), description='Owner details'),
    'amenities': fields.List(fields.String, description='List of amenity IDs'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

# -----------------------------
# Crear y listar lugares (Places)
# -----------------------------
@api.route('/')
class PlaceList(Resource):
    @jwt_required()  # Solo usuarios autenticados pueden crear lugares
    @api.expect(place_model, validate=True)
    def post(self):
        """Create a new place."""
        user_id = get_jwt_identity()  # Obtener ID del usuario autenticado
        facade = current_app.facade
        data = api.payload
        data['owner_id'] = user_id  # 🔥 Asignar usuario autenticado como dueño

        try:
            place = facade.create_place(data)
            return place if isinstance(place, dict) else place.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400

    def get(self):
        """Retrieve all places (public endpoint)."""
        facade = current_app.facade
        places = facade.get_all_places()
        if not isinstance(places, list):
            return {"error": "Unexpected data format"}, 500
        return places, 200

# -----------------------------
# Obtener, actualizar o eliminar un place específico
# -----------------------------
@api.route('/<string:place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        """Retrieve a specific place by ID (public endpoint)."""
        place = current_app.facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place if isinstance(place, dict) else place.to_dict(), 200

    @jwt_required()
    @api.expect(place_model, validate=True)
    def put(self, place_id):
        """Update an existing place (only the owner can update)."""
        user_id = get_jwt_identity()  # Obtener ID del usuario autenticado
        facade = current_app.facade
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        if place.get("owner", {}).get("id") != user_id:  # 🔥 Verificar el propietario correctamente
            return {"error": "Unauthorized action"}, 403

        # 🔥 Actualizar solo los campos permitidos
        for key, value in api.payload.items():
            if key not in ["id", "owner"]:  # 🔥 No permitir modificar `id` ni `owner`
                place[key] = value

        updated_place = facade.update_place(place_id, user_id, place)  # 🔥 Guardar cambios
        return {"message": "Place updated successfully", "place": updated_place}, 200

    @jwt_required()
    def delete(self, place_id):
        """Delete a place (only the owner can delete)."""
        user_id = get_jwt_identity()  # Obtener ID del usuario autenticado
        facade = current_app.facade
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        if place.get("owner", {}).get("id") != user_id:  # 🔥 Verificar permisos antes de eliminar
            return {"error": "Unauthorized action"}, 403

        facade.delete_place(place_id, user_id)
        return {"message": "Place deleted successfully"}, 200
