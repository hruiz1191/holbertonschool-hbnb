from flask import request, jsonify, current_app
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade  # ✅ Importar la instancia de HBnBFacade

api = Namespace('places', description='Place management')

# Modelo de Place
place_model = api.model('Place', {
    'id': fields.String(),
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'owner_id': fields.String(required=True, description='Owner ID'),
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})

# -----------------------------
# Crear y listar lugares (Places)
# -----------------------------
@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model, validate=True)
    def post(self):
        """Create a new place (Only authenticated users)."""
        current_user = get_jwt_identity()
        if not current_user or 'id' not in current_user:
            return {"error": "Invalid user session"}, 401

        data = api.payload
        data['owner_id'] = current_user["id"]

        # ✅ Validar que latitud y longitud existan
        if 'latitude' not in data or 'longitude' not in data:
            return {"error": "Latitude and longitude are required"}, 400

        try:
            place = facade.create_place(data)
            return place, 201
        except ValueError as e:
            return {"error": str(e)}, 400

    def get(self):
        """Retrieve all places (public endpoint)."""
        places = facade.get_all_places()
        return places, 200

# -----------------------------
# Obtener, actualizar o eliminar un place específico
# -----------------------------
@api.route('/<string:place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        """Retrieve a specific place by ID (public endpoint)."""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place, 200

    @jwt_required()
    @api.expect(place_model, validate=True)
    def put(self, place_id):
        """Update an existing place (Owner or Admin)."""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        # ✅ Verificar permisos: Solo dueño o admin pueden actualizar
        is_admin = current_user.get("is_admin", False)
        is_owner = place['owner_id'] == current_user["id"]

        if not (is_admin or is_owner):
            return {"error": "Unauthorized action"}, 403

        # ✅ Actualizar solo campos permitidos
        updated_data = {key: value for key, value in api.payload.items() if key != "owner_id"}
        updated_place = facade.update_place(place_id, current_user["id"], updated_data)
        return {"message": "Place updated successfully", "place": updated_place}, 200

    @jwt_required()
    def delete(self, place_id):
        """Delete a place (Owner or Admin)."""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        # ✅ Verificar permisos: Solo dueño o admin pueden eliminar
        is_admin = current_user.get("is_admin", False)
        is_owner = place['owner_id'] == current_user["id"]

        if not (is_admin or is_owner):
            return {"error": "Unauthorized action"}, 403

        facade.delete_place(place_id, current_user["id"])
        return {"message": "Place deleted successfully"}, 200
