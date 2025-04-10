from flask import request, jsonify, current_app
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade  # Importar la instancia de HBnBFacade

api = Namespace('places', description='Place management')

# Modelo de Place
place_model = api.model('Place', {
    'id': fields.String(),
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
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
        current_user_id = get_jwt_identity()
        print("[DEBUG] Usuario autenticado (ID):", current_user_id)

        if not current_user_id:
            print("[ERROR] Sesión de usuario inválida.")
            return {"error": "Invalid user session"}, 401

        data = api.payload
        print("[DEBUG] Payload recibido:", data)

        # Asignar automáticamente el user_id
        data['user_id'] = current_user_id
        print("[DEBUG] Payload con user_id agregado:", data)

        if 'latitude' not in data or 'longitude' not in data:
            print("[ERROR] Faltan coordenadas en la creación del lugar.")
            return {"error": "Latitude and longitude are required"}, 400

        try:
            place = facade.create_place(data)
            print("[SUCCESS] Lugar creado correctamente:", place)
            return place, 201
        except ValueError as e:
            print("[ERROR] Error al crear lugar:", str(e))
            return {"error": str(e)}, 400

    def get(self):
        """Retrieve all places (public endpoint)."""
        print("[DEBUG] Solicitando lista de todos los lugares...")
        places = facade.get_all_places()
        print("[SUCCESS] Lista de lugares obtenida:", places)
        return places, 200

# -----------------------------
# Obtener, actualizar o eliminar un place específico
# -----------------------------
@api.route('/<string:place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        """Retrieve a specific place by ID (public endpoint)."""
        print(f"[DEBUG] Solicitando detalles del lugar ID: {place_id}")
        place = facade.get_place(place_id)
        if not place:
            print("[ERROR] Lugar no encontrado.")
            return {"error": "Place not found"}, 404
        print("[SUCCESS] Lugar encontrado:", place)
        return place, 200

    @jwt_required()
    @api.expect(place_model, validate=True)
    def put(self, place_id):
        """Update an existing place (Owner or Admin)."""
        current_user_id = get_jwt_identity()
        print("[DEBUG] Usuario que quiere actualizar (ID):", current_user_id)

        place = facade.get_place(place_id)
        if not place:
            print("[ERROR] Lugar a actualizar no encontrado.")
            return {"error": "Place not found"}, 404

        is_admin = place.get('is_admin', False)
        is_owner = place['user_id'] == current_user_id

        if not (is_admin or is_owner):
            print("[ERROR] Acción no autorizada para actualizar.")
            return {"error": "Unauthorized action"}, 403

        updated_data = {key: value for key, value in api.payload.items() if key != "user_id"}
        print("[DEBUG] Data para actualizar:", updated_data)

        updated_place = facade.update_place(place_id, current_user_id, updated_data)
        print("[SUCCESS] Lugar actualizado:", updated_place)
        return {"message": "Place updated successfully", "place": updated_place}, 200

    @jwt_required()
    def delete(self, place_id):
        """Delete a place (Owner or Admin)."""
        current_user_id = get_jwt_identity()
        print("[DEBUG] Usuario que quiere eliminar (ID):", current_user_id)

        place = facade.get_place(place_id)
        if not place:
            print("[ERROR] Lugar a eliminar no encontrado.")
            return {"error": "Place not found"}, 404

        is_admin = place.get('is_admin', False)
        is_owner = place['user_id'] == current_user_id

        if not (is_admin or is_owner):
            print("[ERROR] Acción no autorizada para eliminar.")
            return {"error": "Unauthorized action"}, 403

        facade.delete_place(place_id, current_user_id)
        print("[SUCCESS] Lugar eliminado correctamente.")
        return {"message": "Place deleted successfully"}, 200
