"""App initialization."""
from flask import Flask, request
from flask_restx import Api
from app.services.facade import HBnBFacade

def create_app():
    app = Flask(__name__)
    api = Api(app)

    app.facade = HBnBFacade()

    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.amenities import api as amenities_ns

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

    # 💥 AQUI VIENE EL MIDDLEWARE DE LOGS
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
        print(f"   Body: {response.get_data(as_text=True)}")
        return response

    return app
