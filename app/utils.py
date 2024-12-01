from functools import wraps
from flask import jsonify, render_template, session, request, redirect, url_for, flash, Config
from flask_jwt_extended import decode_token, get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import JWTDecodeError, NoAuthorizationError

def manejar_errores(func):
    """
    Decorador para manejar excepciones y devolver respuestas JSON uniformes.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ve:
            return jsonify({"message": str(ve), "result": None}), 400
        except Exception as e:
            return jsonify({"message": f"Error inesperado en {func.__name__}: {e}", "result": None}), 500
    return wrapper

def with_jwt(func):
    """
    Decorador para agregar automáticamente el token JWT de la sesión a los headers de las solicitudes.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = session.get('jwt')
        if not token:
            flash("Por favor, inicia sesión para acceder a esta página.", "warning")
            return render_template('error.html', error_code=401, message="No estás autenticado."), 401
        # Agregar el token al header Authorization
        request.headers = {**request.headers, "Authorization": f"Bearer {token}"}
        return func(*args, **kwargs)
    return wrapper

def validar_jwt(token):
    """
    Valida un token JWT, devolviendo `True` si es válido o levantando una excepción si no lo es.
    """
    try:
        decode_token(token)
        return True
    except JWTDecodeError:
        session.clear()
        flash("Tu sesión ha expirado. Por favor, inicia sesión de nuevo.", "warning")
        return False
    except NoAuthorizationError:
        session.clear()
        flash("Token inválido. Por favor, inicia sesión de nuevo.", "danger")
        return False

def obtener_usuario_actual():
    """
    Obtiene la información del usuario actual desde el token JWT.
    """
    try:
        usuario = get_jwt_identity()
        if not usuario:
            raise ValueError("Usuario no autenticado.")
        return usuario
    except Exception as e:
        return None

def requerir_rol_api(*roles):
    """
    Decorador para rutas de la API que verifica el rol del usuario desde el JWT.
    """
    def decorador(f):
        @wraps(f)
        def envoltura(*args, **kwargs):
            verify_jwt_in_request()
            usuario = get_jwt_identity()
            if usuario.get('rol') not in roles:
                return jsonify({"message": "Acceso denegado"}), 403
            return f(*args, **kwargs)
        return envoltura
    return decorador

def requerir_rol_web(*roles):
    """
    Decorador para rutas web que verifica el rol del usuario desde la sesión.
    """
    def decorador(f):
        @wraps(f)
        def envoltura(*args, **kwargs):
            usuario = session.get('usuario')
            if not usuario:
                # Usuario no autenticado
                return render_template('error.html', error_code=401, message="No estás autenticado."), 401
            if usuario.get('rol') not in roles:
                # Usuario autenticado pero sin permisos
                return render_template('error.html', error_code=403, message="Acceso denegado."), 403
            return f(*args, **kwargs)
        return envoltura
    return decorador
