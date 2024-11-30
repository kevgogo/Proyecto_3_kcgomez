from flask import render_template, redirect, url_for, flash, request, session
import requests

def registrar_rutas_web(app):
    """
    Registra las rutas web directamente en la aplicación Flask.
    """
    # ------------------- Rutas para la Plataforma Web -------------------

    @app.route('/')
    def index():
        """Página principal que muestra los primeros 4 productos desde la API."""
        try:
            # Generar la URL completa para listar productos
            api_url = f"{request.host_url}api/productos"
            response = requests.get(api_url)
            response.raise_for_status()
            productos = response.json()[:4]
        except requests.RequestException:
            flash("Error al obtener productos desde la API.", "danger")
            productos = []
        return render_template('index.html', productos=productos)

    @app.route('/ingredientes')
    def ingredientes():
        """Página que muestra todos los ingredientes desde la API."""
        try:
            api_url = f"{request.host_url}api/ingredientes"
            response = requests.get(api_url)
            response.raise_for_status()
            ingredientes = response.json()
        except requests.RequestException:
            flash("Error al obtener ingredientes desde la API.", "danger")
            ingredientes = []
        return render_template('ingredientes.html', ingredientes=ingredientes)

    @app.route('/productos')
    def productos():
        """Página que muestra todos los productos desde la API."""
        try:
            api_url = f"{request.host_url}api/productos"
            response = requests.get(api_url)
            response.raise_for_status()
            productos = response.json()
        except requests.RequestException:
            flash("Error al obtener productos desde la API.", "danger")
            productos = []
        return render_template('productos.html', productos=productos)

    @app.route('/vender')
    def lista_para_vender():
        """Página que muestra productos disponibles para vender desde la API."""
        try:
            api_url = f"{request.host_url}api/productos"
            response = requests.get(api_url)
            response.raise_for_status()
            productos = response.json()
        except requests.RequestException:
            flash("Error al obtener productos desde la API.", "danger")
            productos = []
        return render_template('vender.html', productos=productos)

    @app.route('/vender/<int:id>', methods=['POST'])
    def vender(id):
        """Procesa la venta de un producto utilizando la API."""
        try:
            api_url = f"{request.host_url}api/productos/{id}/vender"
            response = requests.post(api_url)
            response.raise_for_status()
            flash(f"Producto con ID {id} vendido exitosamente.", "success")
        except requests.RequestException:
            flash(f"Error al vender el producto con ID {id}.", "danger")
        return redirect(url_for('lista_para_vender'))
