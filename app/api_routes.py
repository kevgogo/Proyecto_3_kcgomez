from flask import Flask, jsonify, request
from controllers.heladeria_controler import HeladeriaController

API_PREFIX = "/api"

def registrar_rutas_api(app):
    """
    Registra las rutas de la API directamente en la aplicación Flask.
    """
    # ------------------- Rutas para Productos -------------------

    @app.route(f"{API_PREFIX}/productos", methods=['GET'])
    def api_listar_productos():
        response, status = HeladeriaController.listar_productos()
        return jsonify(response), status

    @app.route(f"{API_PREFIX}/productos/<int:id>", methods=['GET'])
    def api_obtener_producto_por_id(id):
        response, status = HeladeriaController.obtener_producto_por_id(id)
        return jsonify(response), status

    @app.route(f"{API_PREFIX}/productos/buscar", methods=['GET'])
    def api_buscar_producto_por_nombre():
        nombre = request.args.get("nombre", "")
        response, status = HeladeriaController.buscar_producto_por_nombre(nombre)
        return jsonify(response), status

    @app.route(f"{API_PREFIX}/productos/calorias/<int:id>", methods=['GET'])
    def api_obtener_calorias_producto(id):
        response, status = HeladeriaController.obtener_calorias_producto(id)
        return jsonify(response), status

    @app.route(f"{API_PREFIX}/productos/rentabilidad/<int:id>", methods=['GET'])
    def api_obtener_rentabilidad_producto(id):
        response, status = HeladeriaController.obtener_rentabilidad_producto(id)
        return jsonify(response), status

    @app.route(f"{API_PREFIX}/productos/costo/<int:id>", methods=['GET'])
    def api_obtener_costo_producto(id):
        response, status = HeladeriaController.obtener_costo_producto(id)
        return jsonify(response), status

    @app.route(f"{API_PREFIX}/productos/vender/<int:id>", methods=['POST'])
    def api_vender_producto_por_id(id):
        response, status = HeladeriaController.vender_producto_por_id(id)
        return jsonify(response), status

    @app.route(f"{API_PREFIX}/productos/reabastecer/<int:id>", methods=['POST'])
    def api_reabastecer_producto(id):
        cantidad = request.json.get("cantidad", 0)
        response, status = HeladeriaController.reabastecer_producto(id, cantidad)
        return jsonify(response), status

    @app.route(f"{API_PREFIX}/productos/renovar/<int:id>", methods=['POST'])
    def api_renovar_inventario_producto(id):
        cantidad = request.json.get("cantidad", 0)
        response, status = HeladeriaController.renovar_inventario_producto(id, cantidad)
        return jsonify(response), status

    # ------------------- Rutas para Ingredientes -------------------

    @app.route(f"{API_PREFIX}/ingredientes", methods=['GET'])
    def api_listar_ingredientes():
        response, status = HeladeriaController.listar_ingredientes()
        return jsonify(response), status

    @app.route(f"{API_PREFIX}/ingredientes/<int:id>", methods=['GET'])
    def api_obtener_ingrediente_por_id(id):
        response, status = HeladeriaController.obtener_ingrediente_por_id(id)
        return jsonify(response), status

    @app.route(f"{API_PREFIX}/ingredientes/buscar", methods=['GET'])
    def api_buscar_ingrediente_por_nombre():
        nombre = request.args.get("nombre", "")
        response, status = HeladeriaController.buscar_ingrediente_por_nombre(nombre)
        return jsonify(response), status

    @app.route(f"{API_PREFIX}/ingredientes/sano/<int:id>", methods=['GET'])
    def api_es_ingrediente_sano(id):
        response, status = HeladeriaController.es_ingrediente_sano(id)
        return jsonify(response), status
