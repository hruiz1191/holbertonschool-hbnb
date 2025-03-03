"""Users API endpoints."""

from flask import current_app, request
from flask_restx import Namespace, Resource, fields

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

    @api.marshal_list_with(user_model)
    def get(self):
        """Retrieve all users."""
        return current_app.facade.get_all_users()

    @api.expect(user_model, validate=True)
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user."""
        user_data = request.get_json()

        existing_users = current_app.facade.get_all_users()
        if any(user['email'] == user_data['email'] for user in existing_users):
            return {'error': 'Email already registered'}, 400

        new_user = current_app.facade.create_user(user_data)
        return new_user.to_dict(), 201


@api.route('/<string:user_id>')
class UserResource(Resource):
    """Single user resource."""

    @api.marshal_with(user_model)
    def get(self, user_id):
        user = current_app.facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict()

    @api.expect(user_model, validate=True)
    @api.marshal_with(user_model)
    def put(self, user_id):
        user_data = request.get_json()
        user = current_app.facade.update_user(user_id, user_data)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict()

    def delete(self, user_id):
        user = current_app.facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        current_app.facade.delete_user(user_id)
        return {'message': 'User deleted successfully'}, 200
