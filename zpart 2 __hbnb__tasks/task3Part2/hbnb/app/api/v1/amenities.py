from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')
facade = HBnBFacade()

# Modelo para la documentación de la API
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Nombre del amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity creado exitosamente')
    @api.response(400, 'Datos inválidos')
    def post(self):
        """Crea un nuevo amenity"""
        try:
            data = api.payload
            amenity = facade.create_amenity(data)
            return {"id": amenity.id, "name": amenity.name}, 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, 'Lista de amenities obtenida exitosamente')
    def get(self):
        """Lista todos los amenities"""
        amenities = facade.get_all_amenities()
        return [{"id": a.id, "name": a.name} for a in amenities], 200

@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity obtenido exitosamente')
    @api.response(404, 'Amenity no encontrado')
    def get(self, amenity_id):
        """Obtiene un amenity por su ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity no encontrado"}, 404
        return {"id": amenity.id, "name": amenity.name}, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity actualizado exitosamente')
    @api.response(404, 'Amenity no encontrado')
    @api.response(400, 'Datos inválidos')
    def put(self, amenity_id):
        """Actualiza un amenity existente"""
        try:
            data = api.payload
            updated_amenity = facade.update_amenity(amenity_id, data)
            if not updated_amenity:
                return {"error": "Amenity no encontrado"}, 404
            return {"message": "Amenity actualizado exitosamente"}, 200
        except ValueError as e:
            return {"error": str(e)}, 400
