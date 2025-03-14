from flask_restx import Namespace, Resource, fields
from flask import current_app

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True),
    'description': fields.String(),
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'owner_id': fields.String(required=True),
    'amenities': fields.List(fields.String)
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    def post(self):
        facade = current_app.facade
        place = facade.create_place(api.payload)
        if not place:
            return {"error": "Owner o amenities no válidos"}, 400
        return place.to_dict(), 201

    def get(self):
        facade = current_app.facade
        return facade.get_all_places(), 200
