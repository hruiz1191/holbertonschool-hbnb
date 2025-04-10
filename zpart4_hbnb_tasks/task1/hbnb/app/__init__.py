import os
from flask import Flask, request, send_from_directory, Blueprint
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config

# Instancias globales
bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class="default"):
    """Factory function para crear una aplicación Flask con configuración específica."""
    
    app = Flask(
        __name__,
        template_folder='../templates',
        static_folder='../static'
    )

    # Cargar configuración
    app.config.from_object(config.get(config_class, "default"))
    app.config["JWT_SECRET_KEY"] = "super-secret-key"  # Cambiar en producción 🔥

    # Inicializar extensiones
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Importar la fachada después de inicializar db
    from app.services.facade import HBnBFacade  
    app.facade = HBnBFacade()

    # --- CREAR BLUEPRINT DE API ---
    api_bp = Blueprint('api', __name__, url_prefix="/api/v1")
    api = Api(
        api_bp,
        title="HBnB API",
        version="1.0",
        description="API de HBnB",
        doc="/doc"  # Swagger disponible en /api/v1/doc
    )

    # Importar y registrar Namespaces
    from app.api.v1 import auth_ns, users_ns, places_ns, reviews_ns, amenities_ns
    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(users_ns, path="/users")
    api.add_namespace(places_ns, path="/places")
    api.add_namespace(reviews_ns, path="/reviews")
    api.add_namespace(amenities_ns, path="/amenities")

    # Registrar el Blueprint de la API
    app.register_blueprint(api_bp)

    # Registrar el Blueprint para vistas web
    from app.web.views import web
    app.register_blueprint(web)

    # Ruta para servir archivos de Swagger UI (opcional si usas carpeta swaggerui)
    @app.route('/swaggerui/<path:filename>')
    def serve_swagger_static(filename):
        return send_from_directory(os.path.join(app.root_path, 'swaggerui'), filename)

    # --- Middleware de Logging ---
    @app.before_request
    def log_request_info():
        print("\nIncoming request:")
        print(f"   Method: {request.method}")
        print(f"   Path: {request.path}")
        print(f"   Headers: {dict(request.headers)}")
        print(f"   Body: {request.get_data(as_text=True)}")

    @app.after_request
    def log_response_info(response):
        print("Outgoing response:")
        print(f"   Status: {response.status}")
        if not response.direct_passthrough:
            print(f"   Body: {response.get_data(as_text=True)}")
        return response

    return app
