from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

api = Namespace("amenities", description="Amenity management")

# Modelo para validación con Flask-RESTx
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description="Amenity name")
})

@api.route('/')
class AmenityList(Resource):
    def get(self):
        """Retrieve all amenities."""
        amenities = facade.get_all_amenities()
        return amenities if amenities else {"message": "No amenities found"}, 200

    @api.expect(amenity_model, validate=True)
    @jwt_required()
    def post(self):
        """Create a new amenity (Admin only)."""
        user_id = get_jwt_identity()  # 🔥 Obtiene el user_id
        current_user = facade.get_user(user_id)  # 🔥 Obtiene el usuario completo

        if not current_user or not current_user.get("is_admin"):
            return {"error": "Admin privileges required"}, 403

        data = request.json
        name = data.get("name")

        if not name:
            return {"error": "Name is required"}, 400

        try:
            amenity = facade.create_amenity(data)
            return {"message": "Amenity created", "amenity": amenity}, 201
        except ValueError as e:
            return {"error": str(e)}, 400


@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    def get(self, amenity_id):
        """Retrieve a specific amenity."""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return amenity, 200

    @api.expect(amenity_model, validate=True)
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity (Admin only)."""
        user_id = get_jwt_identity()  # 🔥 Obtiene el user_id
        current_user = facade.get_user(user_id)  # 🔥 Obtiene el usuario completo

        if not current_user or not current_user.get("is_admin"):
            return {"error": "Admin privileges required"}, 403

        data = request.json
        updated_amenity = facade.update_amenity(amenity_id, data)

        if updated_amenity:
            return {"message": "Amenity updated", "amenity": updated_amenity}, 200
        return {"error": "Amenity not found"}, 404  # ✅ Cambio aquí

    @jwt_required()
    def delete(self, amenity_id):
        """Delete a specific amenity (Admin only)."""
        user_id = get_jwt_identity()  # 🔥 Obtiene el user_id
        current_user = facade.get_user(user_id)  # 🔥 Obtiene el usuario completo

        if not current_user or not current_user.get("is_admin"):
            return {"error": "Admin privileges required"}, 403

        if facade.delete_amenity(amenity_id):
            return {"message": "Amenity deleted successfully"}, 200
        return {"error": "Amenity not found"}, 404

