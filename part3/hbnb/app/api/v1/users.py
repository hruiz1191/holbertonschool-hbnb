"""Users API endpoints."""

from flask import current_app, request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity  # Importamos get_jwt_identity

api = Namespace('users', description='User operations')

user_model = api.model(
    'User',
    {
        'id': fields.String(),
        'first_name': fields.String(),
        'last_name': fields.String(),
        'email': fields.String(),
        'is_admin': fields.Boolean(),
        'created_at': fields.String(),
        'updated_at': fields.String()
    }
)

@api.route('/')
class UserList(Resource):
    """User list resource."""

    @jwt_required()  # Protegido para usuarios autenticados
    @api.marshal_list_with(user_model)
    def get(self):
        """Retrieve all users (passwords are not included)."""
        return current_app.facade.get_all_users()

    @api.expect(user_model, validate=True)
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user with hashed password."""
        user_data = request.get_json()

        # Verificar si falta la contraseña
        if 'password' not in user_data:
            return {'error': 'Password is required'}, 400

        # Verificar si el email ya está registrado
        existing_users = current_app.facade.get_all_users()
        if any(user['email'] == user_data['email'] for user in existing_users):
            return {'error': 'Email already registered'}, 400

        # Crear usuario con contraseña hasheada
        response, status_code = current_app.facade.create_user(user_data)
        return response, status_code  # Se usa el formato correcto

@api.route('/<string:user_id>')
class UserResource(Resource):
    """Single user resource."""

    @jwt_required()  # Protege la ruta con JWT
    @api.marshal_with(user_model)
    def get(self, user_id):
        """Retrieve user information by ID, ensuring the user can only access their own profile."""
        current_user_id = get_jwt_identity()  # Obtiene el ID del usuario autenticado

        # 🔹 Si el usuario autenticado intenta acceder a otro usuario, devuelve un error 403
        if str(current_user_id) != user_id:
            return {"error": "Unauthorized access"}, 403

        user = current_app.facade.get_user(user_id)

        if not user:
            return {"error": "User not found"}, 404

        return user.to_dict(), 200

    @jwt_required()  # Solo usuarios autenticados pueden modificar información
    @api.expect(user_model, validate=True)
    @api.marshal_with(user_model)
    def put(self, user_id):
        """Update an existing user (hash password if updated)."""
        current_user_id = get_jwt_identity()

        if str(current_user_id) != user_id:
            return {"error": "Unauthorized access"}, 403

        user_data = request.get_json()
        user = current_app.facade.update_user(user_id, user_data)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict()

    @jwt_required()  # Solo usuarios autenticados pueden eliminar usuarios
    def delete(self, user_id):
        """Delete a user by ID."""
        current_user_id = get_jwt_identity()

        if str(current_user_id) != user_id:
            return {"error": "Unauthorized access"}, 403

        user = current_app.facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        current_app.facade.delete_user(user_id)
        return {'message': 'User deleted successfully'}, 200
