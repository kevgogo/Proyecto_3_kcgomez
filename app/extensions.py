from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config

# Instancias de las extensiones
db = SQLAlchemy()
# bcrypt = Bcrypt()
jwt = JWTManager()

def initialize_extensions(app):
    """
    Inicializa las extensiones Flask con la aplicación.
    """
    db.init_app(app)
    Config.conditional_print("SQLAlchemy initialized successfully.")
    # bcrypt.init_app(app)
    # Config.conditional_print("BCrypt initialized successfully.")
    jwt.init_app(app)
    Config.conditional_print("JWT initialized successfully.")

    # Configuraciones adicionales para JWT
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """
        Maneja el caso de que el token JWT haya expirado.
        """
        return {
            "message": "El token ha expirado. Por favor, inicia sesión nuevamente.",
            "result": None
        }, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """
        Maneja el caso de que el token JWT sea inválido.
        """
        return {
            "message": "Token inválido. Por favor, inicia sesión nuevamente.",
            "result": None
        }, 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        """
        Maneja el caso de que el token JWT falte en la solicitud.
        """
        return {
            "message": "Se requiere un token para acceder a este recurso.",
            "result": None
        }, 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        """
        Maneja el caso de que el token JWT haya sido revocado.
        """
        return {
            "message": "El token ha sido revocado. Por favor, inicia sesión nuevamente.",
            "result": None
        }, 401
