import os
from flask import Flask, request, send_from_directory
from flask_restx import Api
from app.services.facade import HBnBFacade
from config import config  # Importamos la configuración

def create_app(config_class="default"):
    """
    Factory function to create a Flask application instance with a given configuration.
    """
    app = Flask(__name__)
    
    # Aplicar configuración basada en la clave proporcionada
    app.config.from_object(config.get(config_class, "default"))

    # Instanciar la API
    api = Api(app, title="HBnB API", version="1.0", description="API de HBnB")

    # Agregar la fachada
    app.facade = HBnBFacade()

    # Importar y registrar namespaces
    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.amenities import api as amenities_ns

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
