import os
from flask import Flask, request, send_from_directory
from flask_restx import Api
from flask_bcrypt import Bcrypt  # Para hash de contraseñas
from flask_jwt_extended import JWTManager  # Para autenticación JWT
from flask_sqlalchemy import SQLAlchemy  # Agregar SQLAlchemy
from flask_migrate import Migrate  # Agregar Flask-Migrate
from config import config  # Importamos la configuración

# Crear instancias globales
bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()  # Definir db aquí para evitar importación circular
migrate = Migrate()

def create_app(config_class="default"):
    """
    Factory function para crear una aplicación Flask con configuración específica.
    """
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates'),
        static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static')
    )

    # Aplicar configuración desde `config.py`
    app.config.from_object(config.get(config_class, "default"))
    app.config["JWT_SECRET_KEY"] = "super-secret-key"  # Asegurar clave secreta

    # Inicializar extensiones en la app
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)  # Inicializar SQLAlchemy
    migrate.init_app(app, db)  # Inicializar Flask-Migrate

    # Importar HBnBFacade dentro de la función para evitar importación circular
    from app.services.facade import HBnBFacade  
    app.facade = HBnBFacade()

    # Importar namespaces después de inicializar la app y la BD
    from app.api.v1 import auth_ns, users_ns, places_ns, reviews_ns, amenities_ns

    # Blueprint web
    from app.web.views import web

    # Instanciar la API con documentación
    
    api = Api(
    app,
    title="HBnB API",
    version="1.0",
    description="API de HBnB",
    prefix="/api/v1",  # <--para ver el index.html
    doc="/api/v1/doc"  # <-- Mueve el Swagger UI aquí
)

    # Registrar namespaces
    api.add_namespace(auth_ns, path="/api/v1/auth")  # Autenticación
    api.add_namespace(users_ns, path="/api/v1/users")  # Usuarios
    api.add_namespace(places_ns, path="/api/v1/places")  # Lugares
    api.add_namespace(reviews_ns, path="/api/v1/reviews")  # Reseñas
    api.add_namespace(amenities_ns, path="/api/v1/amenities")  # Amenidades

    # web folder for views
    app.register_blueprint(web)

    # Servir archivos estáticos de Swagger UI
    @app.route('/swaggerui/<path:filename>')
    def serve_swagger_static(filename):
        return send_from_directory(os.path.join(app.root_path, 'swaggerui'), filename)

    # Middleware para registrar logs de cada solicitud
    @app.before_request
    def log_request_info():
        print("\n Incoming request:")
        print(f"   Method: {request.method}")
        print(f"   Path: {request.path}")
        print(f"   Headers: {dict(request.headers)}")
        print(f"   Body: {request.get_data(as_text=True)}")

    @app.after_request
    def log_response_info(response):
        print("Outgoing response:")
        print(f"   Status: {response.status}")

        # Evitar error con direct_passthrough
        if not response.direct_passthrough:
            print(f"   Body: {response.get_data(as_text=True)}")
            
        return response

    return app
