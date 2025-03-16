from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade

api = Namespace('auth', description='Authentication operations')

# Modelo para login
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
        facade = HBnBFacade()

        print(f"[DEBUG] Intentando autenticar usuario con email: {credentials['email']}")

        user = facade.get_user_by_email(credentials['email'])

        if not user:
            print("[DEBUG] Usuario no encontrado en base de datos.")
            return {'error': 'User not found'}, 404

        print(f"[DEBUG] Verificando contraseña para usuario: {user.to_dict()}")

        if not user.verify_password(credentials['password']):
            print("[DEBUG] Contraseña incorrecta.")
            return {'error': 'Invalid credentials'}, 401

        # 🔥 Corrección: identity debe ser un string y usar additional_claims
        access_token = create_access_token(identity=str(user.id), additional_claims={"is_admin": user.is_admin})
        print(f"[DEBUG] Usuario autenticado exitosamente. Generado token: {access_token}")
        
        return {'access_token': access_token}, 200

# Modelo para registro de usuario
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
        facade = HBnBFacade()

        print(f"[DEBUG] Intentando registrar usuario con email: {user_data['email']}")

        if facade.get_user_by_email(user_data['email']):
            print("[DEBUG] Usuario ya existe en la base de datos.")
            return {'error': 'User already exists'}, 400

        response, status_code = facade.create_user(user_data)  # Desempacamos la tupla
        print(f"[DEBUG] Usuario registrado con éxito: {response}")  # Ahora imprimimos un diccionario válido

        return response, status_code  # Retornamos correctamente

# Endpoint protegido con JWT
@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()  # Requiere JWT
    def get(self):
        """Endpoint protegido"""
        current_user = get_jwt_identity()  # Devuelve el user.id como string
        print(f"[DEBUG] Acceso permitido para usuario con ID: {current_user}")
        return {'message': f'Hello, user {current_user}'}, 200
