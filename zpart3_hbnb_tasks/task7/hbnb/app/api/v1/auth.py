from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services.facade import facade  # ✅ Importamos la instancia única de HBnBFacade

api = Namespace('auth', description='Authentication operations')

# 🔹 Modelo para login
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Autentica al usuario y retorna un JWT"""
        credentials = api.payload

        print(f"[DEBUG] Intentando autenticar usuario con email: {credentials['email']}")

        user = facade.get_user_by_email(credentials["email"])
        if not user:
            print("[DEBUG] Usuario no encontrado en la base de datos.")
            return {'error': 'Invalid credentials'}, 401

        print(f"[DEBUG] Verificando contraseña para usuario: {user.to_dict()}")

        # 🔥 Verificamos la contraseña correctamente
        if not user.verify_password(credentials["password"]):
            print(f"[DEBUG] Contraseña incorrecta para usuario: {user.email}")
            return {"error": "Invalid credentials"}, 401

        access_token = create_access_token(identity=str(user.id), additional_claims={"is_admin": user.is_admin})
        print(f"[DEBUG] Usuario autenticado exitosamente. Token generado.")

        return {'access_token': access_token}, 200


# 🔹 Modelo para registro de usuario
register_model = api.model('Register', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'is_admin': fields.Boolean(default=False, description='Is admin')
})

@api.route('/register')
class Register(Resource):
    @api.expect(register_model)
    def post(self):
        """Registra un nuevo usuario"""
        user_data = api.payload

        print(f"[DEBUG] Intentando registrar usuario con email: {user_data['email']}")

        if facade.get_user_by_email(user_data['email']):
            print("[DEBUG] Error: Usuario ya existe en la base de datos.")
            return {'error': 'User already exists'}, 400

        response, status_code = facade.create_user(user_data)
        print(f"[DEBUG] Usuario registrado con éxito: {response}")

        return response, status_code


# 🔹 Endpoint protegido con JWT
@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """Endpoint protegido"""
        current_user = get_jwt_identity()
        print(f"[DEBUG] Acceso permitido para usuario con ID: {current_user}")
        return {'message': f'Hello, user {current_user}'}, 200
