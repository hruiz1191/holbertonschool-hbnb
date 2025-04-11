from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade  # ✅ Importamos la instancia global

api = Namespace('users', description='User operations')

# 🔹 Modelo para validar y documentar en Swagger
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'is_admin': fields.Boolean(default=False, description='Is admin')
})

@api.route('/')
class UserList(Resource):
    """Manejo de usuarios."""

    @jwt_required()  # Solo usuarios autenticados pueden ver la lista
    def get(self):
        """Retrieve all users (sin contraseñas)."""
        print("[DEBUG] Obteniendo lista de usuarios...")

        users = facade.get_all_users()
        if not users:
            print("[DEBUG] No hay usuarios registrados.")
            return {"message": "No users found"}, 200

        print(f"[DEBUG] {len(users)} usuarios encontrados.")
        return users, 200

    @api.expect(user_model)
    def post(self):
        """Registrar un nuevo usuario."""
        user_data = request.json
        print(f"[DEBUG] Intentando registrar usuario con email: {user_data.get('email')}")

        if 'password' not in user_data:
            print("[DEBUG] Error: La contraseña es obligatoria.")
            return {'error': 'Password is required'}, 400

        # Verificar si el email ya está registrado
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            print("[DEBUG] Error: El email ya está registrado.")
            return {'error': 'Email already registered'}, 400

        # Crear usuario
        response, status_code = facade.create_user(user_data)
        print(f"[DEBUG] Usuario registrado con éxito: {response}")

        return response, status_code


@api.route('/<string:user_id>')
class UserResource(Resource):
    """Manejo de un usuario específico."""

    @jwt_required()
    def get(self, user_id):
        """Obtener información de un usuario por ID (solo el dueño puede acceder)."""
        current_user_id = get_jwt_identity()
        print(f"[DEBUG] Intento de acceso a usuario {user_id} por usuario autenticado {current_user_id}")

        if str(current_user_id) != user_id:
            print("[DEBUG] Acceso denegado: No autorizado.")
            return {"error": "Unauthorized access"}, 403

        user = facade.get_user(user_id)
        if not user:
            print("[DEBUG] Error: Usuario no encontrado.")
            return {"error": "User not found"}, 404

        print(f"[DEBUG] Información del usuario encontrada: {user}")
        return user, 200

    @jwt_required()
    @api.expect(user_model)
    def put(self, user_id):
        """Actualizar un usuario (No se puede modificar email ni contraseña)."""
        current_user_id = get_jwt_identity()
        print(f"[DEBUG] Usuario {current_user_id} intenta actualizar usuario {user_id}")

        if str(current_user_id) != user_id:
            print("[DEBUG] Acceso denegado: No autorizado para actualizar.")
            return {"error": "Unauthorized access"}, 403

        data = request.get_json()
        if 'email' in data or 'password' in data:
            print("[DEBUG] Error: No se permite modificar email ni contraseña.")
            return {"error": "You cannot modify email or password"}, 400

        updated_user = facade.update_user(user_id, data)
        if not updated_user:
            print("[DEBUG] Error: Usuario no encontrado.")
            return {'error': 'User not found'}, 404

        print(f"[DEBUG] Usuario actualizado correctamente: {updated_user}")
        return updated_user, 200

    @jwt_required()
    def delete(self, user_id):
        """Eliminar un usuario por ID (solo el dueño puede eliminar su cuenta)."""
        current_user_id = get_jwt_identity()
        print(f"[DEBUG] Usuario {current_user_id} intenta eliminar usuario {user_id}")

        if str(current_user_id) != user_id:
            print("[DEBUG] Acceso denegado: No autorizado para eliminar usuario.")
            return {"error": "Unauthorized access"}, 403

        user = facade.get_user(user_id)
        if not user:
            print("[DEBUG] Error: Usuario no encontrado para eliminar.")
            return {'error': 'User not found'}, 404

        facade.delete_user(user_id)
        print(f"[DEBUG] Usuario {user_id} eliminado exitosamente.")
        return {'message': 'User deleted successfully'}, 200
