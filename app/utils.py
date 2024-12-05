from datetime import datetime, timezone
import json
from functools import wraps
from flask import jsonify, render_template, session, request, redirect, url_for, flash, Config
from flask_jwt_extended import decode_token, get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import JWTDecodeError, NoAuthorizationError

def es_solicitud_api():
    """
    Determina si la solicitud actual es para una API.
    """
    return request.path.startswith('/api') or request.content_type == 'application/json' or "Authorization" in request.headers

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
    
def with_jwt_api(func):
    """
    Decorador para validar el token JWT en solicitudes API.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization', "")
        if not token and not token.startswith('Bearer '):
            return {"error": "Token inválido", "message": "El token proporcionado no es válido o ha expirado."}, 401
        if not validar_jwt(token.split(' ')[1]):
            return {"error": "Token inválido", "message": "El token proporcionado no es válido o ha expirado."}, 401
        return func(*args, **kwargs)
    return wrapper

def with_jwt_web(func):
    """
    Decorador para validar el token JWT en solicitudes web.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = session.get('jwt')
        if not token:
            # Redirigir a la página de error si el token no está presente
            return render_template('error.html', error_code=401, message="No estás autenticado."), 401
        if not validar_jwt(token):
            # Redirigir a la página de error si el token es inválido
            return render_template('error.html', error_code=401, message="Token inválido o expirado."), 401
        return func(*args, **kwargs)
    return wrapper

def requerir_rol_api(*roles):
    """
    Decorador para rutas de la API que verifica el rol del usuario desde el JWT.
    """
    def decorador(f):
        @wraps(f)
        def envoltura(*args, **kwargs):
            verify_jwt_in_request()
            decoded = get_jwt_identity()
            user = json.loads(decoded)
            if user.get('rol') not in roles:
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
            token = session.get('jwt')
            if not token:
                # Renderizar directamente el error
                return render_template('error.html', error_code=401, message="No estás autenticado."), 401
            if token and validar_jwt(token):
                decoded = decode_token(token)
                user = json.loads(decoded.get('sub'))
                if user.get('rol') not in roles:
                    return render_template('error.html', error_code=403, message="Acceso denegado."), 403
            return f(*args, **kwargs)
        return envoltura
    return decorador

def injectar_jwt_headers(func):
    """
    Decorador para inyectar automáticamente el token JWT de la sesión en los encabezados.
    Verifica que el token no haya expirado.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = session.get('jwt')
        if not token:
            flash("No estás autenticado. Por favor, inicia sesión.", "danger")
            return redirect(url_for('web.web_login'))
        
        try:
            # Decodificar el token para verificar su validez
            decoded_token = decode_token(token)
            exp = decoded_token.get("exp")
            if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(tz=timezone.utc):
                flash("Tu sesión ha expirado. Por favor, inicia sesión de nuevo.", "danger")
                return redirect(url_for('web.web_login'))
        except JWTDecodeError:
            flash("Token inválido. Por favor, inicia sesión de nuevo.", "danger")
            return redirect(url_for('web.web_login'))
        except NoAuthorizationError:
            flash("Token inválido. Por favor, inicia sesión de nuevo.", "danger")
            return redirect(url_for('web.web_login'))
        
        # Inyectar el token en los encabezados globales
        kwargs["headers"] = {
            "Authorization": f"Bearer {token}"
        }

        return func(*args, **kwargs)
    return wrapper