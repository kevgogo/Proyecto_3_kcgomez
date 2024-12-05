from flask import json, redirect, render_template, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, decode_token
from flask_bcrypt import Bcrypt
from jwt import ExpiredSignatureError, InvalidTokenError
from app.utils import es_solicitud_api, validar_jwt
from config import Config

# Instancias de las extensiones
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def initialize_extensions(app):
    """
    Inicializa las extensiones Flask con la aplicación.
    """
    db.init_app(app)
    Config.conditional_print("SQLAlchemy initialized successfully.")
    bcrypt.init_app(app)
    Config.conditional_print("BCrypt initialized successfully.")
    jwt.init_app(app)
    Config.conditional_print("JWT initialized successfully.")

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        if es_solicitud_api():
            # Respuesta JSON para la API
            return {"error": "Token expirado", "message": "El token ha expirado. Por favor, renueva tu sesión."}, 401
        else:
            # Renderizado para vistas web
            return render_template('error.html', error_code=401, message="El token ha expirado. Por favor, inicia sesión nuevamente."), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        if es_solicitud_api():
            return {"error": "Token inválido", "message": "El token proporcionado no es válido."}, 401
        else:
            return render_template('error.html', error_code=401, message="Token inválido. Por favor, inicia sesión nuevamente."), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        if es_solicitud_api():
            return {"error": "Token faltante", "message": "No se proporcionó un token para acceder a este recurso."}, 401
        else:
            return render_template('error.html', error_code=401, message="Se requiere un token para acceder a este recurso."), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        if es_solicitud_api():
            return {"error": "Token revocado", "message": "El token ha sido revocado. Por favor, inicia sesión nuevamente."}, 401
        else:
            return render_template('error.html', error_code=401, message="El token ha sido revocado. Por favor, inicia sesión nuevamente."), 401
    
    @app.context_processor
    def inject_user():
        """
        Inyecta información del usuario decodificada desde el token JWT usando Flask-JWT-Extended.
        """
        token = session.get('jwt')
        if not token:
            return {
                'usuario_autenticado': False,
                'usuario_rol': "",
                'usuario_nombre' : ""
            }
        
        try:
            if token and validar_jwt(token):
                decoded = decode_token(token)
                user = json.loads(decoded.get('sub'))
                usuario_rol = user.get('rol')  # Extraer el rol del usuario
                usuario_name = user.get('username')  # Extraer el username del usuario
                return {
                    'usuario_autenticado': True,
                    'usuario_rol': # `usuario_rol` is a variable that is used to store the role of the
                    # authenticated user. It is extracted from the decoded JWT token.
                    # The role information is typically included in the token payload
                    # when the user logs in or authenticates. The role can be used to
                    # determine the permissions and access rights of the user within
                    # the application. In this code snippet, `usuario_rol` is being
                    # extracted from the decoded JWT token's payload and then used to
                    # provide information about the user's role in the application.
                    usuario_rol,
                    'usuario_nombre' : usuario_name
                }
        except ExpiredSignatureError:
            return {
                'usuario_autenticado': False,
                'usuario_rol': "",
                'usuario_nombre' : ""
            }
        except InvalidTokenError:
            return {
                'usuario_autenticado': False,
                'usuario_rol': "",
                'usuario_nombre' : ""
            }
        