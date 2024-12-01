from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.utils import requerir_rol_web, with_jwt
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
        return render_template('error.html', message="Error al cargar los productos principales.")

@web.route('/ingredientes')
@requerir_rol_web('admin', 'empleado')
def web_ingredientes():
    """
    Página que muestra todos los ingredientes.
    """
    try:
        api_url = Config.URLBuilder("ingredientes")
        response = requests.get(api_url)
        response.raise_for_status()
        ingredientes = response.json().get("result", [])
        return render_template('ingredientes.html', ingredientes=ingredientes)
    except Exception as e:
        flash("No se pudieron cargar los ingredientes. Inténtalo de nuevo más tarde.", "danger")
        return render_template('error.html', message="Error al cargar los ingredientes.")

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
        return render_template('error.html', message="Error al cargar los productos.")

@web.route('/vender')
@with_jwt
@requerir_rol_web('admin', 'empleado', 'cliente')
def web_lista_para_vender():
    """
    Página que muestra los productos disponibles para la venta.
    """
    try:
        api_url = Config.URLBuilder("productos")
        response = requests.get(api_url)
        response.raise_for_status()
        productos = response.json().get("result", [])
        return render_template('vender.html', productos=productos)
    except Exception as e:
        flash("No se pudieron cargar los productos para la venta. Inténtalo de nuevo más tarde.", "danger")
        return render_template('error.html', message="Error al cargar los productos para la venta.")

@web.route('/vender/<int:id>', methods=['POST'])
@with_jwt
@requerir_rol_web('admin', 'empleado', 'cliente')
def web_vender_producto(id):
    """
    Procesa la venta de un producto.
    """
    try:
        api_url = Config.URLBuilder(f"productos/vender/{id}")
        response = requests.post(api_url)
        response.raise_for_status()
        flash("Producto vendido exitosamente.", "success")
        return redirect(url_for('web.web_lista_para_vender'))
    except Exception as e:
        flash(f"Error al vender el producto con ID {id}: {e}", "danger")
        return render_template('error.html', message=f"Error al vender el producto con ID {id}.")

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
            flash("Inicio de sesión exitoso.", "success")
            return redirect(url_for('web.index'))
        except Exception as e:
            flash("Error al iniciar sesión. Por favor, verifica tus credenciales.", "danger")
            return render_template('error.html', message="Error al iniciar sesión.")
    return render_template('login.html')

@web.route('/logout')
def web_logout():
    """
    Cierra la sesión del usuario.
    """
    session.clear()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for('web.index'))

@web.route('/error')
def web_error():
    """
    Página genérica de error.
    """
    message = request.args.get("message", "Ha ocurrido un error inesperado.")
    return render_template('error.html', message=message)

@web.route('/unauthorized')
def unauthorized():
    return render_template('error.html', error_code=401, message="Acceso denegado."), 401

@web.route('/forbidden')
def forbidden():
    return render_template('error.html', error_code=403, message="No tienes permisos para acceder."), 403