from flask import render_template
from markupsafe import escape
from app import app


# Ruta principal - muestra productos
@app.route('/')
def index():
    from controllers.heladeria_controler import HeladeriaController
    productos = HeladeriaController.listar_productos()[:4]
    return render_template('index.html', productos=productos)

# Ruta para listar ingredientes
@app.route('/ingredientes')
def ingredientes():
    from controllers.heladeria_controler import HeladeriaController

    ingredientes = HeladeriaController.listar_ingredientes()
    return render_template('ingredientes.html', ingredientes=ingredientes)

# Ruta para listar productos
@app.route('/productos')
def productos():
    from controllers.heladeria_controler import HeladeriaController

    productos = HeladeriaController.listar_productos()
    return render_template('productos.html', productos=productos)

# Ruta para vender un producto
@app.route('/vender')
def lista_para_vender():
    from controllers.heladeria_controler import HeladeriaController

    productos = HeladeriaController.listar_productos()
    return render_template('vender.html', productos=productos)

# Ruta para procesar la venta de un producto específico
@app.route('/vender/<nombre_producto>')
def vender(nombre_producto):
    from controllers.heladeria_controler import HeladeriaController

    nombre_producto = escape(nombre_producto)  
    try:
        mensaje = HeladeriaController.vender_producto(nombre_producto)
        return render_template('resultado.html', mensaje=mensaje)
    except ValueError as e:
        return render_template('resultado.html', mensaje=str(e))
