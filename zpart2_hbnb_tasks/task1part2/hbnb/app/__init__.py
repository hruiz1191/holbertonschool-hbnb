from flask import Flask
from flask_restx import Api

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', 
              description='API para la aplicación HBnB', doc='/api/v1/')

    # Aquí se agregarán los namespaces o blueprints con los endpoints.
    return app
