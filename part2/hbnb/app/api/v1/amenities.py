from flask_restx import Namespace, Resource, fields
from flask import current_app

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True)
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    def post(self):
        """Crear un nuevo amenity"""
        facade = current_app.facade
        amenity = facade.create_amenity(api.payload)  # Le pasa un diccionario {'name': 'WiFi'}
        return amenity.to_dict(), 201

    def get(self):
        """Listar todos los amenities"""
        facade = current_app.facade
        return facade.get_all_amenities(), 200
