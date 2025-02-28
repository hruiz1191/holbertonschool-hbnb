from flask import Flask
from flask_restx import Api
from app.api.v1.amenities import api as amenities_ns

def create_app():
    app = Flask(__name__)

    api = Api(
        app,
        title='HBnB API',
        version='1.0',
        description='API para la gestión de HBnB'
    )

    # Registrar namespaces aquí
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

    return app


