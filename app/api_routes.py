from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from config import Config
from controllers.heladeria_controler import HeladeriaController
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils import requerir_rol_api
from models.usuario import Usuario

API_PREFIX = Config.API_PREFIX
api = Blueprint('api', __name__, url_prefix=f"/{API_PREFIX}")

# ------------------- Rutas para Autenticación -------------------

@api.route('/login', methods=['POST'])
def login():
    """
    Autentica al usuario y devuelve un token JWT.
    """
    datos = request.json
    username = datos.get("username")
    password = datos.get("password")

    usuario = Usuario.query.filter_by(username=username).first()
    if not usuario:
        return jsonify({"message": "Usuario no encontrado"}), 401

    # Verificar contraseña
    if not check_password_hash(usuario.password, password):
    # if not bcrypt.check_password_hash(usuario.password, password):
        print(f"Error: Contraseña incorrecta para el usuario {username}")
        return jsonify({"message": "Credenciales inválidas"}), 401

    rol = usuario.obtener_rol()
    access_token = create_access_token(identity={"id": usuario.id, "username": usuario.username, "rol": rol})
    return jsonify({"message": "Login exitoso", "access_token": access_token}), 200

# ------------------- Rutas para Productos -------------------

@api.route('/productos', methods=['GET'])
def listar_productos():
    """
    Lista todos los productos disponibles (accesible para cualquiera).
    """
    response, status = HeladeriaController.listar_productos()
    return jsonify(response), status

@api.route('/productos/<int:id>', methods=['GET'])
@jwt_required()
@requerir_rol_api('admin', 'empleado')
def obtener_producto_por_id(id):
    """
    Obtiene un producto por su ID (admin y empleado).
    """
    response, status = HeladeriaController.obtener_producto_por_id(id)
    return jsonify(response), status

@api.route('/productos/buscar', methods=['GET'])
@jwt_required()
@requerir_rol_api('admin', 'empleado')
def buscar_producto_por_nombre():
    """
    Busca un producto por su nombre (admin y empleado).
    """
    nombre = request.args.get("nombre", "")
    response, status = HeladeriaController.buscar_producto_por_nombre(nombre)
    return jsonify(response), status

@api.route('/productos/calorias/<int:id>', methods=['GET'])
@jwt_required()
@requerir_rol_api('admin', 'empleado', 'cliente')
def obtener_calorias_producto(id):
    """
    Obtiene las calorías de un producto por su ID (admin, empleado y cliente).
    """
    response, status = HeladeriaController.obtener_calorias_producto(id)
    return jsonify(response), status

@api.route('/productos/rentabilidad/<int:id>', methods=['GET'])
@jwt_required()
@requerir_rol_api('admin')
def obtener_rentabilidad_producto(id):
    """
    Obtiene la rentabilidad de un producto por su ID (solo admin).
    """
    response, status = HeladeriaController.obtener_rentabilidad_producto(id)
    return jsonify(response), status

@api.route('/productos/costo/<int:id>', methods=['GET'])
@jwt_required()
@requerir_rol_api('admin', 'empleado')
def obtener_costo_producto(id):
    """
    Obtiene el costo de producción de un producto por su ID (admin y empleado).
    """
    response, status = HeladeriaController.obtener_costo_producto(id)
    return jsonify(response), status

@api.route('/productos/vender/<int:id>', methods=['POST'])
@jwt_required()
@requerir_rol_api('admin', 'empleado', 'cliente')
def vender_producto_por_id(id):
    """
    Vende un producto por su ID (admin, empleado y cliente).
    """
    response, status = HeladeriaController.vender_producto_por_id(id)
    return jsonify(response), status

@api.route('/productos/reabastecer/<int:id>', methods=['POST'])
@jwt_required()
@requerir_rol_api('admin', 'empleado')
def reabastecer_producto(id):
    """
    Reabastece un producto por su ID (admin y empleado).
    """
    cantidad = request.json.get("cantidad", 0)
    response, status = HeladeriaController.reabastecer_producto(id, cantidad)
    return jsonify(response), status

@api.route('/productos/renovar/<int:id>', methods=['POST'])
@jwt_required()
@requerir_rol_api('admin', 'empleado')
def renovar_inventario_producto(id):
    """
    Renueva el inventario de un producto por su ID (admin y empleado).
    """
    cantidad = request.json.get("cantidad", 0)
    response, status = HeladeriaController.renovar_inventario_producto(id, cantidad)
    return jsonify(response), status

# ------------------- Rutas para Ingredientes -------------------

@api.route('/ingredientes', methods=['GET'])
@jwt_required()
@requerir_rol_api('admin', 'empleado')
def listar_ingredientes():
    """
    Lista todos los ingredientes disponibles (admin y empleado).
    """
    response, status = HeladeriaController.listar_ingredientes()
    return jsonify(response), status

@api.route('/ingredientes/<int:id>', methods=['GET'])
@jwt_required()
@requerir_rol_api('admin', 'empleado')
def obtener_ingrediente_por_id(id):
    """
    Obtiene un ingrediente por su ID (admin y empleado).
    """
    response, status = HeladeriaController.obtener_ingrediente_por_id(id)
    return jsonify(response), status

@api.route('/ingredientes/buscar', methods=['GET'])
@jwt_required()
@requerir_rol_api('admin', 'empleado')
def buscar_ingrediente_por_nombre():
    """
    Busca un ingrediente por su nombre (admin y empleado).
    """
    nombre = request.args.get("nombre", "")
    response, status = HeladeriaController.buscar_ingrediente_por_nombre(nombre)
    return jsonify(response), status

@api.route('/ingredientes/sano/<int:id>', methods=['GET'])
@jwt_required()
@requerir_rol_api('admin', 'empleado')
def es_ingrediente_sano(id):
    """
    Verifica si un ingrediente es considerado sano (admin y empleado).
    """
    response, status = HeladeriaController.es_ingrediente_sano(id)
    return jsonify(response), status
