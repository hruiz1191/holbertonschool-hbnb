from flask import Blueprint
from flask_restx import Api
from app.api.v1.places import places_ns
from app.api.v1.reviews import reviews_ns

# Crea el Blueprint principal para la API
api_routes = Blueprint('api', __name__, url_prefix='/api/v1')

# Crea el objeto Api para manejar los endpoints
api = Api(api_routes,
          version='1.0',
          title='HBnB Clone API',
          description='API para lugares, reseñas y usuarios')

# Añade los namespaces (subrutas organizadas)
api.add_namespace(places_ns, path='/places')
api.add_namespace(reviews_ns, path='/reviews')
api.add_namespace(places_reviews_ns, path='/places')  # 
