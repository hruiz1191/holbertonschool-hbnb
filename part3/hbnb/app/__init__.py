import os
from flask import Flask, request, send_from_directory
from flask_restx import Api
from flask_bcrypt import Bcrypt  # Para hash de contraseñas
from flask_jwt_extended import JWTManager  # Para autenticación JWT
from config import config  # Importamos la configuración

# Importar todos los namespaces de una vez desde api/v1/__init__.py
from app.api.v1 import auth_ns, users_ns, places_ns, reviews_ns, amenities_ns

# Crear instancias globales de bcrypt y JWTManager
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class="default"):
    """
    Factory function to create a Flask application instance with a given configuration.
    """
    app = Flask(__name__)

    # Aplicar configuración basada en la clave proporcionada
    app.config.from_object(config.get(config_class, "default"))

    # Inicializar bcrypt y JWT en la app
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Importar HBnBFacade dentro de la función para evitar import circular
    from app.services.facade import HBnBFacade  
    app.facade = HBnBFacade()

    # Instanciar la API con documentación
    api = Api(app, title="HBnB API", version="1.0", description="API de HBnB")

    # Registrar namespaces
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

    # Servir archivos estáticos de Swagger UI
    @app.route('/swaggerui/<path:filename>')
    def serve_swagger_static(filename):
        return send_from_directory(os.path.join(app.root_path, 'swaggerui'), filename)

    # Middleware para registrar logs de cada solicitud
    @app.before_request
    def log_request_info():
        print("\n⬅️ Incoming request:")
        print(f"   Method: {request.method}")
        print(f"   Path: {request.path}")
        print(f"   Headers: {dict(request.headers)}")
        print(f"   Body: {request.get_data(as_text=True)}")

    @app.after_request
    def log_response_info(response):
        print("➡️ Outgoing response:")
        print(f"   Status: {response.status}")

        # Evitar error con direct_passthrough
        if not response.direct_passthrough:
            print(f"   Body: {response.get_data(as_text=True)}")
            
        return response

    return app
