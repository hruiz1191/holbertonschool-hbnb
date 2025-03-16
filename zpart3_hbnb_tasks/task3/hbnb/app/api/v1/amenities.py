from flask_restx import Namespace, Resource, fields
from flask import current_app, request

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description="Amenity name")
})


@api.route('/')
class AmenityList(Resource):
    def get(self):
        """Retrieve all amenities."""
        facade = current_app.facade
        return facade.get_all_amenities(), 200

    @api.expect(amenity_model, validate=True)
    def post(self):
        """Create a new amenity."""
        facade = current_app.facade
        amenity = facade.create_amenity(request.json)
        return amenity.to_dict(), 201


@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    def delete(self, amenity_id):
        """Delete a specific amenity."""
        facade = current_app.facade
        facade.delete_amenity(amenity_id)
        return {"message": "Amenity deleted successfully"}, 200

    @api.expect(amenity_model, validate=True)
    def put(self, amenity_id):
        """Update an amenity."""
        facade = current_app.facade
        data = request.json

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404

        amenity.name = data.get('name', amenity.name)
        amenity.save()  # Actualizar timestamps

        return amenity.to_dict(), 200
