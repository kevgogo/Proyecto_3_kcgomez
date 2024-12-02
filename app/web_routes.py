import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_jwt_extended import decode_token
from app.utils import injectar_jwt_headers, requerir_rol_web, validar_jwt, with_jwt_web
from config import Config
import requests

web = Blueprint('web', __name__)

@web.route('/')
def index():
    """
    Página principal que muestra los primeros 4 productos.
    """
    try:
        api_url = Config.URLBuilder("productos")
        response = requests.get(api_url)
        response.raise_for_status()
        productos = response.json().get("result", [])[:4]
        return render_template('index.html', productos=productos)
    except Exception as e:
        flash("No se pudieron cargar los productos principales. Inténtalo de nuevo más tarde.", "danger")
        return render_template('error.html', error_code=500, message="No se pudieron cargar los productos principales. Inténtalo de nuevo más tarde."), 500

@web.route('/ingredientes')
@injectar_jwt_headers
@requerir_rol_web('admin', 'empleado')
def web_ingredientes(**kwargs):
    """
    Página que muestra todos los ingredientes.
    """
    try:
        api_url = Config.URLBuilder("ingredientes")
        headers = kwargs.get('headers', {})
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        ingredientes = response.json().get("result", [])
        return render_template('ingredientes.html', ingredientes=ingredientes)
    except Exception as e:
        flash("No se pudieron cargar los ingredientes. Inténtalo de nuevo más tarde.", "danger")
        return render_template('error.html', error_code=500, message="Error al cargar los ingredientes. Intenta más tarde."), 500


@web.route('/productos')
def web_productos():
    """
    Página que muestra todos los productos.
    """
    try:
        api_url = Config.URLBuilder("productos")
        response = requests.get(api_url)
        response.raise_for_status()
        productos = response.json().get("result", [])
        return render_template('productos.html', productos=productos)
    except Exception as e:
        flash("No se pudieron cargar los productos. Inténtalo de nuevo más tarde.", "danger")
        return render_template('error.html', error_code=500, message="Error al cargar los productos. Intenta más tarde."), 500

@web.route('/vender')
@injectar_jwt_headers
@with_jwt_web
@requerir_rol_web('admin', 'empleado', 'cliente')
def web_lista_para_vender(**kwargs):
    """
    Página que muestra los productos disponibles para la venta.
    """
    try:
        api_url = Config.URLBuilder("productos")
        headers = kwargs.get('headers', {})
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        productos = response.json().get("result", [])
        return render_template('vender.html', productos=productos)
    except Exception as e:
        flash("No se pudieron cargar los productos para la venta. Inténtalo de nuevo más tarde.", "danger")
        return render_template('error.html', error_code=500, message=f"Error al cargar los productos para la venta. Intenta más tarde."), 500

@web.route('/vender/<int:id>', methods=['POST'])
@injectar_jwt_headers
@with_jwt_web
@requerir_rol_web('admin', 'empleado', 'cliente')
def web_vender_producto(id, **kwargs):
    """
    Procesa la venta de un producto.
    """
    try:
        api_url = Config.URLBuilder(f"productos/vender/{id}")
        headers = kwargs.get('headers', {})
        response = requests.post(api_url, headers=headers)
        response.raise_for_status()
        usuario_rol = session.get('usuario_rol')
        if usuario_rol == "cliente":
            flash("Producto comprado exitosamente.", "success")
        else:
            flash("Producto vendido exitosamente.", "success")
        return redirect(url_for('web.web_lista_para_vender'))
    except Exception as e:
        flash(f"Error al vender el producto con ID {id}: {e}", "danger")
        return render_template('error.html', error_code=500, message=f"Error al vender el producto con ID {id}. Intenta más tarde."), 500

@web.route('/login', methods=['GET', 'POST'])
def web_login():
    """
    Página de inicio de sesión.
    """
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        try:
            api_url = Config.URLBuilder("login")
            response = requests.post(api_url, json={"username": username, "password": password})
            response.raise_for_status()

            # Guardar el token JWT en la sesión
            session['jwt'] = response.json().get("access_token")

            token = session.get('jwt')
            if not token:
                # Renderizar directamente el error
                return render_template('error.html', error_code=401, message="No estás autenticado."), 401
            if token and validar_jwt(token):
                flash("Inicio de sesión exitoso.", "success")

                decoded = decode_token(token)
                user = json.loads(decoded.get('sub'))
                session['usuario_rol'] = user.get('rol')
                if user.get('rol') in ["admin", "empleado"]:
                    return redirect(url_for('web.dashboard'))
                return redirect(url_for('web.index'))
        except Exception as e:
            flash("Error al iniciar sesión. Por favor, verifica tus credenciales.", "danger")
            return redirect(url_for('web.web_login', message="Error al iniciar sesión."))
    return render_template('login.html')

@web.route('/dashboard')
@injectar_jwt_headers
@requerir_rol_web('admin', 'empleado')  # Solo administradores y empleados pueden acceder
def dashboard(**kwargs):
    """
    Muestra el dashboard con estadísticas.
    """
    try:
        # Construir la URL de la API
        api_url = Config.URLBuilder("/dashboard/estadisticas")
        
        # Obtener los encabezados del decorador
        headers = kwargs.get('headers', {})

        # Hacer la solicitud a la API
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Levantar excepción si la solicitud falla
        
        # Procesar los datos obtenidos
        result = response.json().get('result', {})
        total_productos = result.get('total_productos', 0)
        total_ingredientes = result.get('total_ingredientes', 0)
        total_usuarios = result.get('total_usuarios', 0)
        total_ventas = result.get('total_ventas', 0)
        productos_mas_vendidos = result.get('productos_mas_vendidos', [])

        return render_template(
            'dashboard.html',
            total_productos=total_productos,
            total_ingredientes=total_ingredientes,
            total_usuarios=total_usuarios,
            productos_mas_vendidos=productos_mas_vendidos,
            total_ventas=total_ventas
        )
    
    except requests.exceptions.HTTPError as e:
        flash("Error al obtener estadísticas del dashboard. Verifica tus permisos.", "danger")
        return redirect(url_for('web.web_login', error_code=e.response.status_code, message=f"HTTPError: {e}"), e.response.status_code)
    except requests.exceptions.ConnectionError:
        flash("No se pudo conectar con la API. Por favor, intenta más tarde.", "danger")
        return redirect(url_for('web.web_login', error_code=500, message="Error de conexión."), 500)
    except Exception as e:
        flash("Ocurrió un error inesperado.", "danger")
        Config.conditional_print(str(e))
        return redirect(url_for('web.web_login', error_code=500, message=str(e)), 500)

@web.route('/logout')
def web_logout():
    """
    Cierra la sesión del usuario.
    """
    session.clear()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for('web.index'))

@web.route('/registro', methods=['GET', 'POST'])
def web_register():
    """
    Maneja el registro de nuevos usuarios desde la interfaz web.
    """
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            username = request.form.get('username')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            rol = request.form.get('rol')

            # Validar contraseñas coinciden
            if password != confirm_password:
                flash("Las contraseñas no coinciden.", "danger")
                return render_template('registro.html')

            # Validar datos completos
            if not username or not password or not rol:
                flash("Por favor, completa todos los campos.", "warning")
                return render_template('registro.html')

            # Enviar datos a la API de registro
            api_url = Config.URLBuilder("/usuarios/registro")
            response = requests.post(api_url, json={
                "username": username,
                "password": password,
                "rol": rol
            })
            response.raise_for_status()

            # Confirmar el registro
            flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
            return redirect(url_for('web.web_login'))
        except Exception as e:
            # Manejar errores de la API o conexión
            flash(f"Error al registrar usuario: {e}", "danger")
            return render_template('registro.html')

    # Si es GET, renderizar formulario de registro
    return render_template('registro.html')
