from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace('auth', description='Authentication operations')

# Modelo Swagger para login
login_model = api.model('Login', {
    'email': fields.String(required=True, example='user@example.com'),
    'password': fields.String(required=True, example='securepassword')
})

# Modelo Swagger para registro
register_model = api.model('Register', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'is_admin': fields.Boolean(default=False)
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Autenticación de usuarios con debug detallado."""
        credentials = api.payload
        email = credentials.get("email")
        password = credentials.get("password")

        print(f"\n[AUTH] Iniciando login para: {email}")

        user = facade.get_user_by_email(email)
        if not user:
            print(f"[AUTH] Usuario no encontrado: {email}")
            return {'error': 'Invalid credentials'}, 401

        print("[AUTH] DEBUG PASSWORD:")
        print(f"- Password ingresado: {password}")
        print(f"- Hash en base de datos: {user.password}")
        print(f"- Longitud del hash: {len(user.password)} caracteres")
        print(f"- ¿Formato bcrypt ($2b$)? {'Sí' if user.password.startswith('$2b$') else 'No'}")

        if not user.password:
            print("[AUTH] ERROR: Password vacío en base de datos.")
            return {"error": "Invalid credentials"}, 401

        if not user.verify_password(password):
            print("[AUTH] ERROR: Falló la verificación de password.")
            return {"error": "Invalid credentials"}, 401

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "is_admin": user.is_admin,
                "email": user.email
            }
        )

        print(f"[AUTH] Login exitoso para: {email}")

        return {
            'access_token': access_token,
            'user_id': str(user.id),
            'is_admin': user.is_admin
        }, 200

@api.route('/register')
class Register(Resource):
    @api.expect(register_model)
    def post(self):
        """Registro de nuevos usuarios."""
        data = api.payload

        print(f"[AUTH] Intentando registrar usuario con email: {data.get('email')}")

        # Validación de existencia
        existing_user = facade.get_user_by_email(data['email'])
        if existing_user:
            print(f"[AUTH] Error: Usuario ya existente: {data['email']}")
            return {'error': 'User already exists'}, 400

        print("[AUTH] No existe, procediendo a crear usuario...")

        # Crear el usuario usando la fachada
        response, status = facade.create_user(data)

        if status == 201:
            print(f"[AUTH] Registro exitoso para: {data['email']}")
        else:
            print(f"[AUTH] Error al registrar usuario: {response}")

        return response, status

@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """Endpoint protegido para usuarios autenticados."""
        current_user = get_jwt_identity()
        print(f"[AUTH] Acceso autorizado para usuario ID: {current_user}")
        return {
            'message': 'Access granted',
            'user_id': current_user
        }, 200
